"""Private Google-response discovery and hardened-importer bridge."""

from __future__ import annotations

from contextlib import contextmanager
import csv
from copy import deepcopy
from dataclasses import dataclass
import os
from pathlib import Path
import tempfile
from typing import Iterator
from uuid import uuid4

import yaml

from .core import VisitStore
from .google_sheets import SheetResponseBatch, SheetResponseSource
from .importer import (
    AtlasImportError,
    ImportResult,
    PrivateMappingStore,
    import_submission,
    submission_fingerprint,
)


STATE_VERSION = "1.0"


@dataclass(frozen=True)
class DiscoveryResult:
    """Safe discovery result containing opaque identifiers and counts only."""

    total_count: int
    processed_count: int
    pending_count: int
    pending_ids: tuple[str, ...]


class PrivateResponseStateStore:
    """Atomic private state for response discovery and processing status."""

    def __init__(self, path: str | Path):
        self.path = Path(path).expanduser()

    def load(self) -> dict:
        try:
            state = yaml.safe_load(self.path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return {"state_version": STATE_VERSION, "responses": []}
        except (OSError, UnicodeError, yaml.YAMLError) as error:
            raise AtlasImportError(
                "Private response state could not be read safely."
            ) from error
        if (
            not isinstance(state, dict)
            or state.get("state_version") != STATE_VERSION
            or not isinstance(state.get("responses"), list)
        ):
            raise AtlasImportError("Private response state is invalid.")
        return state

    def save(self, state: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary_name = tempfile.mkstemp(
            dir=self.path.parent, prefix=".response-state-", suffix=".tmp"
        )
        try:
            with os.fdopen(
                descriptor, "w", encoding="utf-8", newline="\n"
            ) as stream:
                yaml.safe_dump(
                    state, stream, sort_keys=False, allow_unicode=True
                )
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary_name, self.path)
        except Exception:
            try:
                os.unlink(temporary_name)
            except FileNotFoundError:
                pass
            raise

    def mark_processed(
        self, response_id: str, *, visit_id: str, source_fingerprint: str
    ) -> None:
        state = self.load()
        matches = [
            item
            for item in state["responses"]
            if item.get("response_id") == response_id
        ]
        if len(matches) != 1:
            raise AtlasImportError("Selected response state was not found.")
        item = matches[0]
        if item.get("source_fingerprint") != source_fingerprint:
            raise AtlasImportError("Selected response state has changed.")
        item["status"] = "processed"
        item["visit_id"] = visit_id
        self.save(state)


@contextmanager
def _private_csv(
    root: Path,
    headings: tuple[str, ...],
    row: tuple[str, ...],
) -> Iterator[Path]:
    root.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        dir=root, prefix=".google-response-", suffix=".csv"
    )
    path = Path(temporary_name)
    try:
        with os.fdopen(
            descriptor, "w", encoding="utf-8", newline=""
        ) as stream:
            writer = csv.writer(stream, lineterminator="\n")
            writer.writerow(headings)
            writer.writerow(row)
            stream.flush()
            os.fsync(stream.fileno())
        yield path
    finally:
        try:
            path.unlink()
        except FileNotFoundError:
            pass


def _fingerprints(
    batch: SheetResponseBatch, private_root: Path
) -> tuple[str, ...]:
    del private_root
    return tuple(
        submission_fingerprint(
            batch.headings,
            {
                heading: row[index].strip()
                for index, heading in enumerate(batch.headings)
            },
        )
        for row in batch.rows
    )


def _synchronise(
    batch: SheetResponseBatch, state_store: PrivateResponseStateStore
) -> tuple[dict, tuple[str, ...]]:
    fingerprints = _fingerprints(batch, state_store.path.parent)
    state = state_store.load()
    existing_by_row = {
        item.get("row_number"): item for item in state["responses"]
    }
    if len(existing_by_row) != len(state["responses"]):
        raise AtlasImportError("Private response state has duplicate rows.")
    if any(
        not isinstance(row_number, int)
        or row_number < 2
        or row_number > len(batch.rows) + 1
        for row_number in existing_by_row
    ):
        raise AtlasImportError(
            "The Google response source no longer matches private state."
        )

    changed = False
    for offset, fingerprint in enumerate(fingerprints, start=2):
        existing = existing_by_row.get(offset)
        if existing is None:
            item = {
                "response_id": f"RSP-{uuid4().hex.upper()}",
                "row_number": offset,
                "source_fingerprint": fingerprint,
                "status": "pending",
                "visit_id": None,
            }
            state["responses"].append(item)
            existing_by_row[offset] = item
            changed = True
        elif existing.get("source_fingerprint") != fingerprint:
            raise AtlasImportError(
                "A Google response changed after it was discovered."
            )
        elif existing.get("status") not in {"pending", "processed"}:
            raise AtlasImportError("Private response state has an invalid status.")
    if changed:
        state_store.save(state)
    return state, fingerprints


def discover_responses(
    source: SheetResponseSource,
    state_store: PrivateResponseStateStore,
) -> DiscoveryResult:
    """Discover response counts and opaque pending IDs without exposing values."""
    batch = source.fetch()
    state, _ = _synchronise(batch, state_store)
    pending = tuple(
        item["response_id"]
        for item in state["responses"]
        if item["status"] == "pending"
    )
    processed_count = sum(
        1 for item in state["responses"] if item["status"] == "processed"
    )
    return DiscoveryResult(
        total_count=len(batch.rows),
        processed_count=processed_count,
        pending_count=len(pending),
        pending_ids=pending,
    )


def import_selected_response(
    source: SheetResponseSource,
    *,
    state_store: PrivateResponseStateStore,
    response_id: str,
    visit_store: VisitStore,
    mapping_store: PrivateMappingStore,
    existing_visit_id: str | None = None,
    place_id: str | None = None,
    media_types: tuple[str, ...] = (),
    dry_run: bool = False,
) -> ImportResult:
    """Pass one explicitly selected response to the hardened importer."""
    batch = source.fetch()
    state, fingerprints = _synchronise(batch, state_store)
    matches = [
        item
        for item in state["responses"]
        if item.get("response_id") == response_id
    ]
    if len(matches) != 1:
        raise AtlasImportError("Selected response ID was not found.")
    selected = matches[0]
    row_index = selected["row_number"] - 2
    fingerprint = fingerprints[row_index]
    if selected["source_fingerprint"] != fingerprint:
        raise AtlasImportError("Selected response changed before import.")

    with _private_csv(
        state_store.path.parent, batch.headings, batch.rows[row_index]
    ) as csv_path:
        result = import_submission(
            csv_path,
            visit_store=visit_store,
            mapping_store=mapping_store,
            place_id=place_id,
            existing_visit_id=existing_visit_id,
            media_types=media_types,
            source_identity=response_id,
            dry_run=dry_run,
        )
    if not dry_run:
        state_store.mark_processed(
            response_id,
            visit_id=result.visit["visit_id"],
            source_fingerprint=fingerprint,
        )
    return ImportResult(
        visit=deepcopy(result.visit),
        private_mapping=deepcopy(result.private_mapping),
        dry_run=result.dry_run,
        idempotent=result.idempotent,
        mapping_path=result.mapping_path,
    )
