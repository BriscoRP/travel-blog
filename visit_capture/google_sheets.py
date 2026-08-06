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

import yaml

from .importer import (
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
        result = run_check(private_directory)
    except GoogleSheetsCheckError as error:
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
