"""Core operations for the Project Atlas Visit Capture Foundation.

The domain operations depend on the VisitStore protocol rather than a storage
technology. YamlVisitStore is the first local adapter and stores structured
records only; it never reads or copies private evidence.
"""

from __future__ import annotations

from copy import deepcopy
from datetime import date, datetime, timezone
import os
from pathlib import Path
import re
import tempfile
from typing import Callable, Protocol

import yaml


SCHEMA_VERSION = "1.0"
OPEN_STATE = "Open"
EVIDENCE_TYPES = frozenset({"photo", "video", "audio", "note"})
DATE_PRECISIONS = frozenset({"day", "month", "year"})

_TOP_LEVEL_FIELDS = frozenset(
    {
        "schema_version",
        "record_version",
        "visit_id",
        "place_id",
        "visit_date",
        "visit_date_precision",
        "state",
        "contributor_ids",
        "evidence",
        "created_at",
        "last_modified_at",
    }
)
_EVIDENCE_FIELDS = frozenset(
    {
        "evidence_id",
        "evidence_type",
        "added_at",
        "captured_on",
        "description",
        "uncertain",
    }
)
_IDENTIFIER_PATTERNS = {
    "visit_id": re.compile(r"^VIS-[A-Z0-9][A-Z0-9-]{2,63}$"),
    "place_id": re.compile(r"^PLC-[A-Z0-9][A-Z0-9-]{2,63}$"),
    "contributor_id": re.compile(r"^CTR-[A-Z0-9][A-Z0-9-]{2,63}$"),
    "evidence_id": re.compile(r"^EVD-[A-Z0-9][A-Z0-9-]{2,63}$"),
}
_DATE_PATTERNS = {
    "day": re.compile(r"^\d{4}-\d{2}-\d{2}$"),
    "month": re.compile(r"^\d{4}-\d{2}$"),
    "year": re.compile(r"^\d{4}$"),
}
_SENSITIVE_DESCRIPTION_PATTERNS = (
    re.compile(r"\b(?:https?|file)://", re.IGNORECASE),
    re.compile(r"\bwww\.", re.IGNORECASE),
    re.compile(r"(?:^|\s)[A-Za-z]:[\\/]"),
    re.compile(r"\\\\"),
    re.compile(r"(?:^|\s)/(?:Users|home|mnt|Volumes)/", re.IGNORECASE),
    re.compile(r"\b\S+@\S+\.\S+\b"),
)


class VisitError(Exception):
    """Base error for Visit Capture operations."""


class VisitValidationError(VisitError):
    """Raised when a Visit record violates the approved minimum contract."""


class VisitAlreadyExistsError(VisitError):
    """Raised when creation would overwrite an existing Visit."""


class VisitNotFoundError(VisitError):
    """Raised when a requested Visit does not exist."""


class DuplicateEvidenceError(VisitError):
    """Raised when an evidence identifier already exists in a Visit."""


class ConcurrentUpdateError(VisitError):
    """Raised when a stale update would overwrite a newer Visit record."""


class VisitStore(Protocol):
    """Storage boundary implemented by local and future private adapters."""

    def create(self, record: dict) -> None:
        """Persist a new record without overwriting an existing Visit."""

    def load(self, visit_id: str) -> dict:
        """Load a Visit record."""

    def save(self, record: dict, expected_record_version: int) -> None:
        """Replace a record only when the stored version matches expectation."""


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _timestamp(clock: Callable[[], datetime]) -> str:
    value = clock()
    if value.tzinfo is None or value.utcoffset() is None:
        raise VisitValidationError("The clock must return a timezone-aware datetime.")
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def _validate_identifier(field: str, value: object, pattern_name: str) -> None:
    if not isinstance(value, str) or not _IDENTIFIER_PATTERNS[pattern_name].fullmatch(
        value
    ):
        prefix = _IDENTIFIER_PATTERNS[pattern_name].pattern.split("-")[0].lstrip("^")
        raise VisitValidationError(
            f"{field} must be an opaque uppercase identifier beginning {prefix}-."
        )


def _validate_timestamp(field: str, value: object) -> None:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise VisitValidationError(f"{field} must be an ISO 8601 UTC timestamp.")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as error:
        raise VisitValidationError(
            f"{field} must be an ISO 8601 UTC timestamp."
        ) from error
    if parsed.utcoffset() != timezone.utc.utcoffset(parsed):
        raise VisitValidationError(f"{field} must use UTC.")


def _validate_visit_date(value: object, precision: object) -> None:
    if precision not in DATE_PRECISIONS:
        raise VisitValidationError(
            "visit_date_precision must be day, month or year."
        )
    if not isinstance(value, str) or not _DATE_PATTERNS[precision].fullmatch(value):
        raise VisitValidationError(
            f"visit_date must match the declared {precision} precision."
        )
    try:
        if precision == "day":
            date.fromisoformat(value)
        elif precision == "month":
            datetime.strptime(value, "%Y-%m")
        else:
            datetime.strptime(value, "%Y")
    except ValueError as error:
        raise VisitValidationError("visit_date is not a valid calendar value.") from error


def _validate_evidence_item(item: object, position: int) -> None:
    if not isinstance(item, dict):
        raise VisitValidationError(f"evidence[{position}] must be a mapping.")
    unknown = set(item) - _EVIDENCE_FIELDS
    if unknown:
        raise VisitValidationError(
            f"evidence[{position}] has unknown fields: {', '.join(sorted(unknown))}."
        )
    required = {"evidence_id", "evidence_type", "added_at", "uncertain"}
    missing = required - set(item)
    if missing:
        raise VisitValidationError(
            f"evidence[{position}] is missing: {', '.join(sorted(missing))}."
        )
    _validate_identifier(
        f"evidence[{position}].evidence_id", item["evidence_id"], "evidence_id"
    )
    if item["evidence_type"] not in EVIDENCE_TYPES:
        allowed = ", ".join(sorted(EVIDENCE_TYPES))
        raise VisitValidationError(
            f"evidence[{position}].evidence_type must be one of: {allowed}."
        )
    _validate_timestamp(f"evidence[{position}].added_at", item["added_at"])
    if not isinstance(item["uncertain"], bool):
        raise VisitValidationError(f"evidence[{position}].uncertain must be boolean.")
    if "captured_on" in item:
        captured_on = item["captured_on"]
        if not isinstance(captured_on, str):
            raise VisitValidationError(
                f"evidence[{position}].captured_on must be an ISO calendar date."
            )
        try:
            date.fromisoformat(captured_on)
        except ValueError as error:
            raise VisitValidationError(
                f"evidence[{position}].captured_on must be an ISO calendar date."
            ) from error
    if "description" in item:
        description = item["description"]
        if not isinstance(description, str) or not description.strip():
            raise VisitValidationError(
                f"evidence[{position}].description must be non-empty text."
            )
        if len(description) > 500:
            raise VisitValidationError(
                f"evidence[{position}].description must not exceed 500 characters."
            )
        if any(
            pattern.search(description)
            for pattern in _SENSITIVE_DESCRIPTION_PATTERNS
        ):
            raise VisitValidationError(
                f"evidence[{position}].description must not contain a URL, "
                "storage path or contact address."
            )


def validate_visit(record: object) -> None:
    """Validate a record against the minimum Visit Capture contract."""
    if not isinstance(record, dict):
        raise VisitValidationError("Visit record must be a mapping.")

    unknown = set(record) - _TOP_LEVEL_FIELDS
    if unknown:
        raise VisitValidationError(
            f"Visit record has unknown fields: {', '.join(sorted(unknown))}."
        )
    missing = _TOP_LEVEL_FIELDS - set(record)
    if missing:
        raise VisitValidationError(
            f"Visit record is missing: {', '.join(sorted(missing))}."
        )
    if record["schema_version"] != SCHEMA_VERSION:
        raise VisitValidationError(f"schema_version must be {SCHEMA_VERSION}.")
    if (
        not isinstance(record["record_version"], int)
        or isinstance(record["record_version"], bool)
        or record["record_version"] < 1
    ):
        raise VisitValidationError("record_version must be a positive integer.")

    _validate_identifier("visit_id", record["visit_id"], "visit_id")
    _validate_identifier("place_id", record["place_id"], "place_id")
    _validate_visit_date(record["visit_date"], record["visit_date_precision"])

    if record["state"] != OPEN_STATE:
        raise VisitValidationError(
            "state must remain Open in the Visit Capture Foundation."
        )

    contributors = record["contributor_ids"]
    if not isinstance(contributors, list) or not contributors:
        raise VisitValidationError(
            "contributor_ids must contain at least one opaque identifier."
        )
    if len(contributors) != len(set(contributors)):
        raise VisitValidationError("contributor_ids must not contain duplicates.")
    for contributor_id in contributors:
        _validate_identifier(
            "contributor_ids item", contributor_id, "contributor_id"
        )

    evidence = record["evidence"]
    if not isinstance(evidence, list):
        raise VisitValidationError("evidence must be a list.")
    evidence_ids = []
    for position, item in enumerate(evidence):
        _validate_evidence_item(item, position)
        evidence_ids.append(item["evidence_id"])
    if len(evidence_ids) != len(set(evidence_ids)):
        raise VisitValidationError("evidence IDs must be unique within a Visit.")

    _validate_timestamp("created_at", record["created_at"])
    _validate_timestamp("last_modified_at", record["last_modified_at"])


def create_visit(
    store: VisitStore,
    *,
    visit_id: str,
    place_id: str,
    visit_date: str,
    visit_date_precision: str,
    contributor_ids: list[str],
    clock: Callable[[], datetime] = _utc_now,
) -> dict:
    """Create one living Open Visit."""
    record = build_open_visit(
        visit_id=visit_id,
        place_id=place_id,
        visit_date=visit_date,
        visit_date_precision=visit_date_precision,
        contributor_ids=contributor_ids,
        clock=clock,
    )
    store.create(record)
    return deepcopy(record)


def build_open_visit(
    *,
    visit_id: str,
    place_id: str,
    visit_date: str,
    visit_date_precision: str,
    contributor_ids: list[str],
    evidence: list[dict] | None = None,
    clock: Callable[[], datetime] = _utc_now,
) -> dict:
    """Build and validate one complete Open Visit without persisting it."""
    timestamp = _timestamp(clock)
    record = {
        "schema_version": SCHEMA_VERSION,
        "record_version": 1,
        "visit_id": visit_id,
        "place_id": place_id,
        "visit_date": visit_date,
        "visit_date_precision": visit_date_precision,
        "state": OPEN_STATE,
        "contributor_ids": list(contributor_ids),
        "evidence": deepcopy(evidence) if evidence is not None else [],
        "created_at": timestamp,
        "last_modified_at": timestamp,
    }
    validate_visit(record)
    return deepcopy(record)


def add_evidence(
    store: VisitStore,
    *,
    visit_id: str,
    evidence_id: str,
    evidence_type: str,
    captured_on: str | None = None,
    description: str | None = None,
    uncertain: bool = False,
    clock: Callable[[], datetime] = _utc_now,
) -> dict:
    """Append an opaque evidence reference to an existing living Visit."""
    record = store.load(visit_id)
    validate_visit(record)
    if any(item["evidence_id"] == evidence_id for item in record["evidence"]):
        raise DuplicateEvidenceError(
            f"Evidence {evidence_id} already exists in Visit {visit_id}."
        )

    expected_version = record["record_version"]
    item = {
        "evidence_id": evidence_id,
        "evidence_type": evidence_type,
        "added_at": _timestamp(clock),
        "uncertain": uncertain,
    }
    if captured_on is not None:
        item["captured_on"] = captured_on
    if description is not None:
        item["description"] = description

    updated = deepcopy(record)
    updated["evidence"].append(item)
    updated["record_version"] = expected_version + 1
    updated["last_modified_at"] = item["added_at"]
    validate_visit(updated)
    store.save(updated, expected_record_version=expected_version)
    return deepcopy(updated)


class YamlVisitStore:
    """Filesystem YAML adapter for structured Visit records.

    The caller supplies the storage root explicitly. A future private repository
    adapter can implement VisitStore without changing the domain operations.
    """

    def __init__(self, root: str | Path):
        self.root = Path(root).expanduser()

    def _path_for(self, visit_id: str) -> Path:
        _validate_identifier("visit_id", visit_id, "visit_id")
        return self.root / f"{visit_id}.yaml"

    def create(self, record: dict) -> None:
        validate_visit(record)
        destination = self._path_for(record["visit_id"])
        self.root.mkdir(parents=True, exist_ok=True)
        file_descriptor, temporary_name = tempfile.mkstemp(
            dir=self.root, prefix=f".{record['visit_id']}-", suffix=".tmp"
        )
        try:
            with os.fdopen(
                file_descriptor, "w", encoding="utf-8", newline="\n"
            ) as stream:
                yaml.safe_dump(
                    record, stream, sort_keys=False, allow_unicode=True
                )
                stream.flush()
                os.fsync(stream.fileno())
            os.link(temporary_name, destination)
        except FileExistsError as error:
            raise VisitAlreadyExistsError(
                f"Visit {record['visit_id']} already exists."
            ) from error
        finally:
            try:
                os.unlink(temporary_name)
            except FileNotFoundError:
                pass

    def load(self, visit_id: str) -> dict:
        source = self._path_for(visit_id)
        try:
            with source.open("r", encoding="utf-8") as stream:
                record = yaml.safe_load(stream)
        except FileNotFoundError as error:
            raise VisitNotFoundError(f"Visit {visit_id} was not found.") from error
        validate_visit(record)
        if record["visit_id"] != visit_id:
            raise VisitValidationError(
                f"Stored Visit ID does not match requested Visit {visit_id}."
            )
        return record

    def save(self, record: dict, expected_record_version: int) -> None:
        validate_visit(record)
        destination = self._path_for(record["visit_id"])
        current = self.load(record["visit_id"])
        if current["record_version"] != expected_record_version:
            raise ConcurrentUpdateError(
                f"Visit {record['visit_id']} changed after it was loaded."
            )

        self.root.mkdir(parents=True, exist_ok=True)
        file_descriptor, temporary_name = tempfile.mkstemp(
            dir=self.root, prefix=f".{record['visit_id']}-", suffix=".tmp"
        )
        try:
            with os.fdopen(
                file_descriptor, "w", encoding="utf-8", newline="\n"
            ) as stream:
                yaml.safe_dump(
                    record, stream, sort_keys=False, allow_unicode=True
                )
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary_name, destination)
        except Exception:
            try:
                os.unlink(temporary_name)
            except FileNotFoundError:
                pass
            raise
