"""Read-only Google Sheets connection checkpoint for Project Atlas.

This module authenticates an owner-operated desktop session and reports only
safe structural information. It does not import responses or access Drive.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
import tempfile
from typing import Protocol

import yaml

from .importer import (
    AtlasImportError,
    LEGACY_VISITORS_COLUMN,
    VISITORS_COLUMN,
    _FIXED_COLUMNS,
)


READ_ONLY_SCOPE = "https://www.googleapis.com/auth/spreadsheets.readonly"
SCOPES = (READ_ONLY_SCOPE,)


class GoogleSheetsCheckError(Exception):
    """Raised when the private read-only connection cannot be verified."""


@dataclass(frozen=True)
class SheetStructure:
    """Safe structural result containing no response values."""

    worksheet_accessible: bool
    heading_count: int
    recognised_heading_count: int
    response_row_count: int


@dataclass(frozen=True)
class SheetResponseBatch:
    """Private in-memory headings and rows returned by a response source."""

    headings: tuple[str, ...]
    rows: tuple[tuple[str, ...], ...]


class SheetResponseSource(Protocol):
    """Provider-independent source boundary for private Form responses."""

    def fetch(self) -> SheetResponseBatch:
        """Return current response headings and rows."""


class GoogleSheetResponseSource:
    """Read-only Google implementation of the private response source."""

    def __init__(self, service, spreadsheet_id: str, worksheet_title: str):
        self.service = service
        self.spreadsheet_id = spreadsheet_id
        self.worksheet_title = worksheet_title

    def fetch(self) -> SheetResponseBatch:
        escaped_title = self.worksheet_title.replace("'", "''")
        from googleapiclient.errors import HttpError

        try:
            result = (
                self.service.spreadsheets()
                .values()
                .get(
                    spreadsheetId=self.spreadsheet_id,
                    range=f"'{escaped_title}'",
                    majorDimension="ROWS",
                )
                .execute()
            )
        except HttpError as error:
            raise GoogleSheetsCheckError(
                "The Google Sheets API request failed."
            ) from error
        values = result.get("values", [])
        if not values:
            raise GoogleSheetsCheckError(
                "The configured response worksheet has no heading row."
            )
        headings = tuple(str(value) for value in values[0])
        rows = []
        for source_row in values[1:]:
            if len(source_row) > len(headings):
                raise GoogleSheetsCheckError(
                    "A response row contains more values than headings."
                )
            padded = tuple(
                str(source_row[index]) if index < len(source_row) else ""
                for index in range(len(headings))
            )
            if any(value for value in padded):
                rows.append(padded)
        return SheetResponseBatch(headings=headings, rows=tuple(rows))


def default_private_directory() -> Path:
    """Return Atlas's private local Google configuration directory."""
    local_app_data = os.environ.get("LOCALAPPDATA")
    if not local_app_data:
        raise GoogleSheetsCheckError(
            "LOCALAPPDATA is unavailable; supply an explicit private directory."
        )
    return Path(local_app_data) / "ProjectAtlas" / "google"


def _repository_root() -> Path:
    return Path(__file__).resolve().parent.parent


def ensure_private_path(path: Path, label: str) -> Path:
    """Reject credential, token and connection paths inside the repository."""
    resolved = path.expanduser().resolve()
    try:
        resolved.relative_to(_repository_root())
    except ValueError:
        return resolved
    raise GoogleSheetsCheckError(
        f"{label} must be stored outside the Project Atlas repository."
    )


def _write_token_atomic(token_path: Path, content: str) -> None:
    token_path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=token_path.parent, prefix=".oauth-token-", suffix=".tmp"
    )
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(content)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, token_path)
    except Exception:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def authenticate(credentials_path: Path, token_path: Path):
    """Authenticate through Google's installed-app flow with read-only scope."""
    credentials_path = ensure_private_path(credentials_path, "OAuth client file")
    token_path = ensure_private_path(token_path, "OAuth token file")
    if not credentials_path.is_file():
        raise GoogleSheetsCheckError(
            "The private OAuth client file was not found."
        )

    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow

    credentials = None
    if token_path.is_file():
        credentials = Credentials.from_authorized_user_file(token_path, SCOPES)
    if credentials and credentials.expired and credentials.refresh_token:
        credentials.refresh(Request())
    elif not credentials or not credentials.valid:
        flow = InstalledAppFlow.from_client_secrets_file(
            credentials_path, SCOPES
        )
        credentials = flow.run_local_server(
            port=0,
            authorization_prompt_message="",
        )
    if not credentials or not credentials.valid:
        raise GoogleSheetsCheckError("Google authentication did not complete.")
    _write_token_atomic(token_path, credentials.to_json())
    return credentials


def load_private_connection(connection_path: Path) -> tuple[str, str]:
    """Load private spreadsheet and worksheet identifiers without printing them."""
    connection_path = ensure_private_path(
        connection_path, "Sheet connection file"
    )
    try:
        data = yaml.safe_load(connection_path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise GoogleSheetsCheckError(
            "The private Sheet connection file was not found."
        ) from error
    except (OSError, UnicodeError, yaml.YAMLError) as error:
        raise GoogleSheetsCheckError(
            "The private Sheet connection file could not be read."
        ) from error
    if not isinstance(data, dict):
        raise GoogleSheetsCheckError(
            "The private Sheet connection file must be a YAML mapping."
        )
    spreadsheet_id = data.get("spreadsheet_id")
    worksheet_title = data.get("worksheet_title")
    if not isinstance(spreadsheet_id, str) or not spreadsheet_id.strip():
        raise GoogleSheetsCheckError("spreadsheet_id is required.")
    if not isinstance(worksheet_title, str) or not worksheet_title.strip():
        raise GoogleSheetsCheckError("worksheet_title is required.")
    return spreadsheet_id.strip(), worksheet_title.strip()


def inspect_structure(service, spreadsheet_id: str, worksheet_title: str) -> SheetStructure:
    """Read headings and timestamp occupancy, never complete response rows."""
    metadata = (
        service.spreadsheets()
        .get(
            spreadsheetId=spreadsheet_id,
            includeGridData=False,
            fields="sheets.properties.title",
        )
        .execute()
    )
    titles = {
        sheet.get("properties", {}).get("title")
        for sheet in metadata.get("sheets", [])
    }
    if worksheet_title not in titles:
        raise GoogleSheetsCheckError(
            "The configured response worksheet was not found."
        )

    escaped_title = worksheet_title.replace("'", "''")
    result = (
        service.spreadsheets()
        .values()
        .batchGet(
            spreadsheetId=spreadsheet_id,
            ranges=[
                f"'{escaped_title}'!1:1",
                f"'{escaped_title}'!A2:A",
            ],
            majorDimension="ROWS",
        )
        .execute()
    )
    ranges = result.get("valueRanges", [])
    headings = ranges[0].get("values", [[]])[0] if ranges else []
    timestamp_rows = ranges[1].get("values", []) if len(ranges) > 1 else []
    expected = set(_FIXED_COLUMNS) | {
        VISITORS_COLUMN,
        LEGACY_VISITORS_COLUMN,
    }
    recognised = sum(1 for heading in headings if heading in expected)
    return SheetStructure(
        worksheet_accessible=True,
        heading_count=len(headings),
        recognised_heading_count=recognised,
        response_row_count=sum(1 for row in timestamp_rows if row),
    )


def run_check(private_directory: Path) -> SheetStructure:
    """Authenticate and inspect the configured real Sheet read-only."""
    private_directory = ensure_private_path(
        private_directory, "Private Google directory"
    )
    credentials = authenticate(
        private_directory / "oauth-client.json",
        private_directory / "oauth-token.json",
    )
    spreadsheet_id, worksheet_title = load_private_connection(
        private_directory / "sheet-connection.yaml"
    )
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError

    try:
        service = build(
            "sheets", "v4", credentials=credentials, cache_discovery=False
        )
        return inspect_structure(service, spreadsheet_id, worksheet_title)
    except HttpError as error:
        raise GoogleSheetsCheckError(
            "The Google Sheets API request failed."
        ) from error


def open_private_google_source(
    private_directory: Path,
) -> GoogleSheetResponseSource:
    """Open the configured read-only Google source without exposing identifiers."""
    private_directory = ensure_private_path(
        private_directory, "Private Google directory"
    )
    credentials = authenticate(
        private_directory / "oauth-client.json",
        private_directory / "oauth-token.json",
    )
    spreadsheet_id, worksheet_title = load_private_connection(
        private_directory / "sheet-connection.yaml"
    )
    from googleapiclient.discovery import build

    service = build(
        "sheets", "v4", credentials=credentials, cache_discovery=False
    )
    return GoogleSheetResponseSource(
        service, spreadsheet_id, worksheet_title
    )


def main(arguments: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Verify read-only access to the private Atlas response Sheet."
    )
    parser.add_argument(
        "--private-dir",
        type=Path,
        default=None,
        help="Private Google configuration directory outside the repository.",
    )
    parser.add_argument(
        "--authenticate-only",
        action="store_true",
        help="Complete read-only OAuth without accessing a spreadsheet.",
    )
    action = parser.add_mutually_exclusive_group()
    action.add_argument(
        "--discover",
        action="store_true",
        help="List opaque pending response IDs without displaying response values.",
    )
    action.add_argument(
        "--import-response",
        metavar="RESPONSE_ID",
        help="Import one explicitly selected opaque response ID.",
    )
    parser.add_argument("--visit-store", type=Path)
    parser.add_argument("--mapping-dir", type=Path)
    parser.add_argument("--existing-visit-id")
    parser.add_argument("--place-id")
    parser.add_argument(
        "--media-type",
        action="append",
        choices=("photo", "video"),
        default=[],
    )
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(arguments)
    try:
        private_directory = args.private_dir or default_private_directory()
        if args.authenticate_only:
            private_directory = ensure_private_path(
                private_directory, "Private Google directory"
            )
            authenticate(
                private_directory / "oauth-client.json",
                private_directory / "oauth-token.json",
            )
            print("Google read-only authentication succeeded.")
            return 0
        if args.discover or args.import_response:
            from .core import YamlVisitStore
            from .google_bridge import (
                PrivateResponseStateStore,
                discover_responses,
                import_selected_response,
            )
            from .importer import YamlPrivateMappingStore

            private_directory = ensure_private_path(
                private_directory, "Private Google directory"
            )
            source = open_private_google_source(private_directory)
            state_store = PrivateResponseStateStore(
                private_directory / "response-state.yaml"
            )
            if args.discover:
                discovery = discover_responses(source, state_store)
                print(f"Total responses: {discovery.total_count}")
                print(f"Processed responses: {discovery.processed_count}")
                print(f"Pending responses: {discovery.pending_count}")
                for response_id in discovery.pending_ids:
                    print(f"Pending response: {response_id}")
                return 0
            if args.visit_store is None or args.mapping_dir is None:
                raise GoogleSheetsCheckError(
                    "--visit-store and --mapping-dir are required for import."
                )
            result = import_selected_response(
                source,
                state_store=state_store,
                response_id=args.import_response,
                visit_store=YamlVisitStore(
                    ensure_private_path(args.visit_store, "Visit store")
                ),
                mapping_store=YamlPrivateMappingStore(
                    ensure_private_path(
                        args.mapping_dir, "Private mapping directory"
                    )
                ),
                existing_visit_id=args.existing_visit_id,
                place_id=args.place_id,
                media_types=tuple(args.media_type),
                dry_run=args.dry_run,
            )
            print(
                "Selected response validated through the hardened importer."
            )
            print(f"Dry run: {'yes' if result.dry_run else 'no'}")
            print(
                "Operation: "
                f"{result.private_mapping.get('operation', 'create')}"
            )
            print(f"Open Visit ID: {result.visit['visit_id']}")
            print(f"Evidence count: {len(result.visit['evidence'])}")
            return 0
        result = run_check(private_directory)
    except (GoogleSheetsCheckError, AtlasImportError) as error:
        print(f"Connection check failed: {error}")
        return 1
    print("Google Sheets read-only connection succeeded.")
    print("Spreadsheet accessible: yes")
    print(
        "Response worksheet accessible: "
        f"{'yes' if result.worksheet_accessible else 'no'}"
    )
    print(f"Heading count: {result.heading_count}")
    print(f"Recognised Atlas headings: {result.recognised_heading_count}")
    print(f"Response row count: {result.response_row_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
