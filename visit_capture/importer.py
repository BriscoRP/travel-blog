"""Safe one-row Atlas Test V1 CSV importer.

Raw form values and provider references are written only to an explicitly
private mapping store. The VisitStore receives opaque identifiers and safe
evidence descriptions only.
"""

from __future__ import annotations

import csv
from copy import deepcopy
from dataclasses import dataclass, replace
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import tempfile
from typing import Callable, Protocol
from urllib.parse import urlparse
from uuid import uuid4

import yaml

from .core import (
    VisitError,
    VisitNotFoundError,
    VisitStore,
    build_open_visit,
    validate_visit,
)


FORM_VERSION = "Atlas Test V1"
MAPPING_VERSION = "1.0"

TIMESTAMP_COLUMN = "Timestamp"
PLACE_COLUMN = "What place did you visit?"
LOCATION_COLUMN = "Where is it?"
VISITORS_COLUMN = "Who went on the visit? (private)"
LEGACY_VISITORS_COLUMN = "Who went on the vist? (private)"
VISIT_DATE_COLUMN = "Date of visit"
EXPERIENCE_COLUMN = "Tell us about your visit"
ADVICE_COLUMN = "What advice would you give someone visiting?"
PARKING_COLUMN = "How did you park?"
TOILETS_COLUMN = "Did you see or use any toilets?"
ACCESSIBILITY_COLUMN = (
    "Did you notice anything that could make access easier or harder?"
)
RECOMMEND_COLUMN = "Would you recommend visiting?"
MEDIA_COLUMN = "Upload photos or videos for Rik to review"
AUDIO_COLUMN = "Add a voice recording (optional)"

_FIXED_COLUMNS = (
    TIMESTAMP_COLUMN,
    PLACE_COLUMN,
    LOCATION_COLUMN,
    VISIT_DATE_COLUMN,
    EXPERIENCE_COLUMN,
    ADVICE_COLUMN,
    PARKING_COLUMN,
    TOILETS_COLUMN,
    ACCESSIBILITY_COLUMN,
    RECOMMEND_COLUMN,
    MEDIA_COLUMN,
    AUDIO_COLUMN,
)
_REQUIRED_VALUES = (
    TIMESTAMP_COLUMN,
    PLACE_COLUMN,
    LOCATION_COLUMN,
    VISIT_DATE_COLUMN,
    EXPERIENCE_COLUMN,
)
_PRIVATE_HEADING_OPTIONS = frozenset(
    {VISITORS_COLUMN, LEGACY_VISITORS_COLUMN}
)
_CONTRIBUTOR_SEPARATOR = re.compile(r"[,;\n]+")
_PROVIDER_REFERENCE_SEPARATOR = re.compile(r",\s*(?=https?://)")


class AtlasImportError(VisitError):
    """Raised when an Atlas Test V1 submission cannot be imported safely."""


class PrivateMappingStore(Protocol):
    """Private idempotency and provenance boundary for importer mappings."""

    def load(self, fingerprint: str) -> dict | None:
        """Return an existing mapping for a source fingerprint."""

    def reserve(self, mapping: dict) -> None:
        """Persist a new pending mapping without overwriting an existing one."""

    def complete(self, fingerprint: str) -> dict:
        """Mark a pending mapping complete."""

    def discard_pending(self, fingerprint: str, import_id: str) -> None:
        """Remove a newly reserved mapping after a failed Visit write."""

    def path_for(self, fingerprint: str) -> Path:
        """Return the private mapping path for reporting."""

    def find_by_visit_id(self, visit_id: str) -> list[dict]:
        """Return private mappings already associated with one Visit."""


@dataclass(frozen=True)
class ParsedSubmission:
    """One validated Atlas Test V1 CSV row."""

    headings: tuple[str, ...]
    values: dict[str, str]
    visitors_heading: str
    submitted_at: str
    visit_date: str
    contributor_labels: tuple[str, ...]
    media_references: tuple[str, ...]
    audio_references: tuple[str, ...]
    fingerprint: str


@dataclass(frozen=True)
class ImportResult:
    """Result returned by dry-run, new import and idempotent re-import."""

    visit: dict
    private_mapping: dict
    dry_run: bool
    idempotent: bool
    mapping_path: Path


def _utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _timestamp(clock: Callable[[], datetime]) -> str:
    value = clock()
    if value.tzinfo is None or value.utcoffset() is None:
        raise AtlasImportError("The importer clock must be timezone-aware.")
    return value.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


def generate_opaque_id(prefix: str) -> str:
    """Generate a random identifier that contains no contributor information."""
    if prefix not in {"VIS", "PLC", "CTR", "EVD", "IMP"}:
        raise AtlasImportError(f"Unsupported opaque identifier prefix: {prefix}.")
    return f"{prefix}-{uuid4().hex.upper()}"


def _normalise_google_datetime(value: str) -> str:
    formats = ("%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M")
    for date_format in formats:
        try:
            parsed = datetime.strptime(value, date_format)
            return parsed.isoformat()
        except ValueError:
            continue
    raise AtlasImportError(
        f"{TIMESTAMP_COLUMN} must use DD/MM/YYYY HH:MM[:SS]."
    )


def _normalise_visit_date(value: str) -> str:
    try:
        return datetime.strptime(value, "%d/%m/%Y").date().isoformat()
    except ValueError as error:
        raise AtlasImportError(
            f"{VISIT_DATE_COLUMN} must use DD/MM/YYYY."
        ) from error


def _split_contributors(value: str) -> tuple[str, ...]:
    labels = tuple(
        label.strip()
        for label in _CONTRIBUTOR_SEPARATOR.split(value)
        if label.strip()
    )
    if not labels:
        raise AtlasImportError("The private visitor field must not be empty.")
    folded = [label.casefold() for label in labels]
    if len(folded) != len(set(folded)):
        raise AtlasImportError("The private visitor field contains duplicates.")
    return labels


def _split_provider_references(value: str, heading: str) -> tuple[str, ...]:
    if not value.strip():
        return ()
    references = tuple(
        item.strip()
        for item in _PROVIDER_REFERENCE_SEPARATOR.split(value)
        if item.strip()
    )
    for reference in references:
        parsed = urlparse(reference)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise AtlasImportError(
                f"{heading} contains an invalid private provider reference."
            )
    return references


def submission_fingerprint(
    headings: tuple[str, ...], values: dict[str, str]
) -> str:
    """Return the stable source fingerprint used for importer idempotency."""
    fingerprint_payload = json.dumps(
        {"headings": headings, "values": values},
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(fingerprint_payload).hexdigest()


def read_single_submission(csv_path: str | Path) -> ParsedSubmission:
    """Read and validate exactly one Atlas Test V1 response from CSV."""
    source = Path(csv_path)
    try:
        with source.open("r", encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            headings = tuple(reader.fieldnames or ())
            rows = list(reader)
    except FileNotFoundError as error:
        raise AtlasImportError(f"CSV file was not found: {source}.") from error
    except (OSError, UnicodeError, csv.Error) as error:
        raise AtlasImportError(f"CSV file could not be read safely: {error}.") from error

    if not headings or any(not heading for heading in headings):
        raise AtlasImportError("CSV must contain a complete header row.")
    if len(headings) != len(set(headings)):
        raise AtlasImportError("CSV contains duplicate headings.")
    if len(rows) != 1:
        raise AtlasImportError(
            f"CSV must contain exactly one submission row; found {len(rows)}."
        )
    if None in rows[0]:
        raise AtlasImportError("CSV row contains more values than headings.")

    visitor_headings = _PRIVATE_HEADING_OPTIONS.intersection(headings)
    if len(visitor_headings) != 1:
        raise AtlasImportError(
            "CSV must contain exactly one supported private visitor heading: "
            f"{VISITORS_COLUMN!r} or {LEGACY_VISITORS_COLUMN!r}."
        )
    visitors_heading = next(iter(visitor_headings))
    expected = set(_FIXED_COLUMNS) | {visitors_heading}
    missing = expected - set(headings)
    unknown = set(headings) - expected
    if missing:
        raise AtlasImportError(
            f"CSV is missing headings: {', '.join(sorted(missing))}."
        )
    if unknown:
        raise AtlasImportError(
            f"CSV has unsupported headings: {', '.join(sorted(unknown))}."
        )

    row = {
        heading: (rows[0].get(heading) or "").strip()
        for heading in headings
    }
    for heading in (*_REQUIRED_VALUES, visitors_heading):
        if not row[heading]:
            raise AtlasImportError(f"{heading} is required.")

    return ParsedSubmission(
        headings=headings,
        values=row,
        visitors_heading=visitors_heading,
        submitted_at=_normalise_google_datetime(row[TIMESTAMP_COLUMN]),
        visit_date=_normalise_visit_date(row[VISIT_DATE_COLUMN]),
        contributor_labels=_split_contributors(row[visitors_heading]),
        media_references=_split_provider_references(
            row[MEDIA_COLUMN], MEDIA_COLUMN
        ),
        audio_references=_split_provider_references(
            row[AUDIO_COLUMN], AUDIO_COLUMN
        ),
        fingerprint=submission_fingerprint(headings, row),
    )


def _evidence_item(
    evidence_id: str,
    evidence_type: str,
    added_at: str,
    description: str,
) -> dict:
    return {
        "evidence_id": evidence_id,
        "evidence_type": evidence_type,
        "added_at": added_at,
        "description": description,
        "uncertain": False,
    }


def _build_new_evidence(
    submission: ParsedSubmission,
    *,
    media_types: tuple[str, ...],
    id_factory: Callable[[str], str],
    imported_at: str,
) -> tuple[list[dict], list[dict]]:
    if len(media_types) != len(submission.media_references):
        raise AtlasImportError(
            "Supply exactly one --media-type (photo or video) for each "
            "uploaded photo/video reference."
        )
    invalid_media_types = set(media_types) - {"photo", "video"}
    if invalid_media_types:
        raise AtlasImportError("Uploaded media type must be photo or video.")

    evidence_mappings = []
    evidence = []
    note_id = id_factory("EVD")
    evidence.append(
        _evidence_item(
            note_id,
            "note",
            imported_at,
            "Atlas Test V1 form response.",
        )
    )
    evidence_mappings.append(
        {
            "evidence_id": note_id,
            "evidence_type": "note",
            "source_heading": "complete form response",
            "provider_reference": None,
        }
    )

    for provider_reference, evidence_type in zip(
        submission.media_references, media_types, strict=True
    ):
        evidence_id = id_factory("EVD")
        evidence.append(
            _evidence_item(
                evidence_id,
                evidence_type,
                imported_at,
                f"Atlas Test V1 uploaded {evidence_type}.",
            )
        )
        evidence_mappings.append(
            {
                "evidence_id": evidence_id,
                "evidence_type": evidence_type,
                "source_heading": MEDIA_COLUMN,
                "provider_reference": provider_reference,
            }
        )

    for provider_reference in submission.audio_references:
        evidence_id = id_factory("EVD")
        evidence.append(
            _evidence_item(
                evidence_id,
                "audio",
                imported_at,
                "Atlas Test V1 voice recording.",
            )
        )
        evidence_mappings.append(
            {
                "evidence_id": evidence_id,
                "evidence_type": "audio",
                "source_heading": AUDIO_COLUMN,
                "provider_reference": provider_reference,
            }
        )
    return evidence, evidence_mappings


def _source_mapping(submission: ParsedSubmission) -> dict:
    return {
        "kind": "atlas_test_v1_csv",
        "form_version": FORM_VERSION,
        "fingerprint": submission.fingerprint,
        "visitors_heading": submission.visitors_heading,
        "submitted_at": submission.submitted_at,
        "headings": list(submission.headings),
        "values": deepcopy(submission.values),
    }


def _build_create_plan(
    submission: ParsedSubmission,
    *,
    place_id: str | None,
    media_types: tuple[str, ...],
    id_factory: Callable[[str], str],
    clock: Callable[[], datetime],
) -> tuple[dict, dict]:
    imported_at = _timestamp(clock)
    visit_id = id_factory("VIS")
    resolved_place_id = place_id or id_factory("PLC")
    contributor_mappings = [
        {
            "private_label": label,
            "contributor_id": id_factory("CTR"),
        }
        for label in submission.contributor_labels
    ]
    evidence, evidence_mappings = _build_new_evidence(
        submission,
        media_types=media_types,
        id_factory=id_factory,
        imported_at=imported_at,
    )

    visit = build_open_visit(
        visit_id=visit_id,
        place_id=resolved_place_id,
        visit_date=submission.visit_date,
        visit_date_precision="day",
        contributor_ids=[
            item["contributor_id"] for item in contributor_mappings
        ],
        evidence=evidence,
        clock=lambda: datetime.fromisoformat(
            imported_at.replace("Z", "+00:00")
        ),
    )
    mapping = {
        "mapping_version": MAPPING_VERSION,
        "import_id": id_factory("IMP"),
        "operation": "create",
        "status": "pending",
        "source": _source_mapping(submission),
        "generated": {
            "visit_id": visit_id,
            "place": {
                "place_id": resolved_place_id,
                "generated": place_id is None,
                "private_name": submission.values[PLACE_COLUMN],
                "private_location": submission.values[LOCATION_COLUMN],
            },
            "contributors": contributor_mappings,
            "evidence": evidence_mappings,
        },
        "planned_visit": deepcopy(visit),
        "imported_at": imported_at,
        "completed_at": None,
    }
    return visit, mapping


def _normalised_label(value: str) -> str:
    return " ".join(value.split()).casefold()


def _find_create_mapping(mappings: list[dict], visit_id: str) -> dict:
    create_mappings = [
        mapping
        for mapping in mappings
        if mapping.get("operation", "create") == "create"
        and mapping.get("generated", {}).get("visit_id") == visit_id
    ]
    if len(create_mappings) != 1:
        raise AtlasImportError(
            "Append requires exactly one private create mapping for the "
            f"existing Visit {visit_id}."
        )
    return create_mappings[0]


def _append_differences(
    submission: ParsedSubmission,
    existing_visit: dict,
    create_mapping: dict,
) -> list[str]:
    differences = []
    private_place = create_mapping.get("generated", {}).get("place", {})
    expected_name = private_place.get("private_name")
    expected_location = private_place.get("private_location")
    submitted_name = submission.values[PLACE_COLUMN]
    submitted_location = submission.values[LOCATION_COLUMN]
    if not isinstance(expected_name, str) or not isinstance(expected_location, str):
        raise AtlasImportError(
            "Existing private Place mapping is incomplete."
        )
    if _normalised_label(expected_name) != _normalised_label(submitted_name):
        differences.append(
            f"place name was {expected_name!r}, submitted {submitted_name!r}"
        )
    if _normalised_label(expected_location) != _normalised_label(
        submitted_location
    ):
        differences.append(
            f"location was {expected_location!r}, "
            f"submitted {submitted_location!r}"
        )
    if existing_visit["visit_date"] != submission.visit_date:
        differences.append(
            f"Visit date was {existing_visit['visit_date']!r}, "
            f"submitted {submission.visit_date!r}"
        )

    existing_contributors = create_mapping.get("generated", {}).get(
        "contributors"
    )
    if not isinstance(existing_contributors, list) or not existing_contributors:
        raise AtlasImportError(
            "Existing private contributor mapping is incomplete."
        )
    existing_labels = {
        _normalised_label(item.get("private_label", ""))
        for item in existing_contributors
    }
    submitted_labels = {
        _normalised_label(label) for label in submission.contributor_labels
    }
    if existing_labels != submitted_labels:
        existing_display = ", ".join(
            item.get("private_label", "<missing>")
            for item in existing_contributors
        )
        submitted_display = ", ".join(submission.contributor_labels)
        differences.append(
            f"visitor set was {existing_display!r}, "
            f"submitted {submitted_display!r}"
        )
    return differences


def _build_append_plan(
    submission: ParsedSubmission,
    *,
    existing_visit: dict,
    create_mapping: dict,
    place_id: str | None,
    media_types: tuple[str, ...],
    id_factory: Callable[[str], str],
    clock: Callable[[], datetime],
) -> tuple[dict, dict]:
    validate_visit(existing_visit)
    if existing_visit["state"] != "Open":
        raise AtlasImportError("Only an Open Visit can receive an append.")

    private_place = create_mapping.get("generated", {}).get("place", {})
    if private_place.get("place_id") != existing_visit["place_id"]:
        raise AtlasImportError(
            "Existing private Place mapping conflicts with the Visit."
        )
    if place_id is not None and place_id != existing_visit["place_id"]:
        raise AtlasImportError(
            "Supplied Place ID conflicts with the existing Visit."
        )

    differences = _append_differences(
        submission, existing_visit, create_mapping
    )
    if differences:
        raise AtlasImportError(
            "Append submission differs from the existing private mapping: "
            + "; ".join(differences)
            + "."
        )

    contributor_lookup = {
        _normalised_label(item["private_label"]): item["contributor_id"]
        for item in create_mapping["generated"]["contributors"]
    }
    contributor_mappings = [
        {
            "private_label": label,
            "contributor_id": contributor_lookup[_normalised_label(label)],
        }
        for label in submission.contributor_labels
    ]
    mapped_ids = {item["contributor_id"] for item in contributor_mappings}
    if mapped_ids != set(existing_visit["contributor_ids"]):
        raise AtlasImportError(
            "Existing private contributor mapping conflicts with the Visit."
        )

    imported_at = _timestamp(clock)
    evidence, evidence_mappings = _build_new_evidence(
        submission,
        media_types=media_types,
        id_factory=id_factory,
        imported_at=imported_at,
    )
    updated_visit = deepcopy(existing_visit)
    updated_visit["evidence"].extend(evidence)
    updated_visit["record_version"] = existing_visit["record_version"] + 1
    updated_visit["last_modified_at"] = imported_at
    validate_visit(updated_visit)

    mapping = {
        "mapping_version": MAPPING_VERSION,
        "import_id": id_factory("IMP"),
        "operation": "append",
        "status": "pending",
        "source": _source_mapping(submission),
        "generated": {
            "visit_id": existing_visit["visit_id"],
            "place": {
                "place_id": existing_visit["place_id"],
                "generated": False,
                "private_name": private_place["private_name"],
                "private_location": private_place["private_location"],
            },
            "contributors": contributor_mappings,
            "evidence": evidence_mappings,
        },
        "base_record_version": existing_visit["record_version"],
        "planned_visit": deepcopy(updated_visit),
        "imported_at": imported_at,
        "completed_at": None,
    }
    return updated_visit, mapping


def _visit_contains_plan(stored: dict, planned: dict) -> bool:
    fixed_fields = (
        "schema_version",
        "visit_id",
        "place_id",
        "visit_date",
        "visit_date_precision",
        "state",
        "contributor_ids",
        "created_at",
    )
    if any(stored.get(field) != planned.get(field) for field in fixed_fields):
        return False
    if stored.get("record_version", 0) < planned.get("record_version", 0):
        return False
    stored_evidence = {
        item.get("evidence_id"): item for item in stored.get("evidence", [])
    }
    return all(
        stored_evidence.get(item.get("evidence_id")) == item
        for item in planned.get("evidence", [])
    )


def import_submission(
    csv_path: str | Path,
    *,
    visit_store: VisitStore,
    mapping_store: PrivateMappingStore,
    place_id: str | None = None,
    existing_visit_id: str | None = None,
    media_types: tuple[str, ...] = (),
    source_identity: str | None = None,
    dry_run: bool = False,
    id_factory: Callable[[str], str] = generate_opaque_id,
    clock: Callable[[], datetime] = _utc_now,
) -> ImportResult:
    """Import one CSV submission into one validated Open Visit."""
    submission = read_single_submission(csv_path)
    if source_identity is not None:
        if not re.fullmatch(r"RSP-[A-F0-9]{32}", source_identity):
            raise AtlasImportError("Source identity must be an opaque response ID.")
        submission = replace(
            submission,
            fingerprint=hashlib.sha256(
                (
                    submission.fingerprint
                    + "\0"
                    + source_identity
                ).encode("utf-8")
            ).hexdigest(),
        )
    existing = mapping_store.load(submission.fingerprint)

    if existing is not None:
        planned_visit = existing.get("planned_visit")
        if not isinstance(planned_visit, dict):
            raise AtlasImportError("Existing private mapping is incomplete.")
        validate_visit(planned_visit)
        mapped_visit_id = planned_visit["visit_id"]
        if (
            existing_visit_id is not None
            and existing_visit_id != mapped_visit_id
        ):
            raise AtlasImportError(
                "Existing source mapping belongs to a different Visit ID."
            )
        if place_id is not None and planned_visit["place_id"] != place_id:
            raise AtlasImportError(
                "Existing import mapping uses a different Place ID."
            )
        mapped_media_types = tuple(
            item["evidence_type"]
            for item in existing.get("generated", {}).get("evidence", [])
            if item.get("source_heading") == MEDIA_COLUMN
        )
        if media_types and media_types != mapped_media_types:
            raise AtlasImportError(
                "Existing import mapping uses different uploaded media types."
            )
        try:
            stored_visit = visit_store.load(planned_visit["visit_id"])
        except VisitNotFoundError:
            if dry_run:
                return ImportResult(
                    visit=deepcopy(planned_visit),
                    private_mapping=deepcopy(existing),
                    dry_run=True,
                    idempotent=True,
                    mapping_path=mapping_store.path_for(submission.fingerprint),
                )
            if existing.get("status") == "complete":
                raise AtlasImportError(
                    "Completed private mapping refers to a missing Visit."
                )
            if existing.get("operation", "create") == "append":
                raise AtlasImportError(
                    "Pending append refers to a missing existing Visit."
                )
            visit_store.create(planned_visit)
            completed = mapping_store.complete(submission.fingerprint)
            return ImportResult(
                visit=deepcopy(planned_visit),
                private_mapping=completed,
                dry_run=False,
                idempotent=True,
                mapping_path=mapping_store.path_for(submission.fingerprint),
            )
        if not _visit_contains_plan(stored_visit, planned_visit):
            operation = existing.get("operation", "create")
            base_version = existing.get("base_record_version")
            if (
                operation == "append"
                and existing.get("status") == "pending"
                and stored_visit["record_version"] == base_version
                and not dry_run
            ):
                visit_store.save(
                    planned_visit, expected_record_version=base_version
                )
                completed = mapping_store.complete(submission.fingerprint)
                return ImportResult(
                    visit=deepcopy(planned_visit),
                    private_mapping=completed,
                    dry_run=False,
                    idempotent=True,
                    mapping_path=mapping_store.path_for(
                        submission.fingerprint
                    ),
                )
            raise AtlasImportError(
                "Existing Visit does not contain its private import plan."
            )
        completed = existing
        if existing.get("status") != "complete" and not dry_run:
            completed = mapping_store.complete(submission.fingerprint)
        return ImportResult(
            visit=deepcopy(stored_visit),
            private_mapping=deepcopy(completed),
            dry_run=dry_run,
            idempotent=True,
            mapping_path=mapping_store.path_for(submission.fingerprint),
        )

    if existing_visit_id is None:
        visit, mapping = _build_create_plan(
            submission,
            place_id=place_id,
            media_types=media_types,
            id_factory=id_factory,
            clock=clock,
        )
    else:
        existing_visit = visit_store.load(existing_visit_id)
        validate_visit(existing_visit)
        mappings = mapping_store.find_by_visit_id(existing_visit_id)
        create_mapping = _find_create_mapping(mappings, existing_visit_id)
        visit, mapping = _build_append_plan(
            submission,
            existing_visit=existing_visit,
            create_mapping=create_mapping,
            place_id=place_id,
            media_types=media_types,
            id_factory=id_factory,
            clock=clock,
        )
    if dry_run:
        preview_mapping = deepcopy(mapping)
        preview_mapping["status"] = "dry-run"
        return ImportResult(
            visit=visit,
            private_mapping=preview_mapping,
            dry_run=True,
            idempotent=False,
            mapping_path=mapping_store.path_for(submission.fingerprint),
        )

    mapping_store.reserve(mapping)
    try:
        if mapping["operation"] == "create":
            visit_store.create(visit)
        else:
            visit_store.save(
                visit,
                expected_record_version=mapping["base_record_version"],
            )
    except Exception:
        mapping_store.discard_pending(
            submission.fingerprint, mapping["import_id"]
        )
        raise
    completed = mapping_store.complete(submission.fingerprint)
    return ImportResult(
        visit=visit,
        private_mapping=completed,
        dry_run=False,
        idempotent=False,
        mapping_path=mapping_store.path_for(submission.fingerprint),
    )


class YamlPrivateMappingStore:
    """Local private YAML journal for idempotency and provider mappings."""

    def __init__(
        self,
        root: str | Path,
        *,
        clock: Callable[[], datetime] = _utc_now,
    ):
        self.root = Path(root).expanduser()
        self.clock = clock

    def path_for(self, fingerprint: str) -> Path:
        if not re.fullmatch(r"[a-f0-9]{64}", fingerprint):
            raise AtlasImportError("Source fingerprint is invalid.")
        return self.root / f"atlas-test-v1-{fingerprint}.private.yaml"

    def _write_atomic(self, destination: Path, mapping: dict) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        file_descriptor, temporary_name = tempfile.mkstemp(
            dir=self.root, prefix=".atlas-import-", suffix=".tmp"
        )
        try:
            with os.fdopen(
                file_descriptor, "w", encoding="utf-8", newline="\n"
            ) as stream:
                yaml.safe_dump(
                    mapping, stream, sort_keys=False, allow_unicode=True
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

    def _write_new_atomic(self, destination: Path, mapping: dict) -> None:
        self.root.mkdir(parents=True, exist_ok=True)
        file_descriptor, temporary_name = tempfile.mkstemp(
            dir=self.root, prefix=".atlas-import-", suffix=".tmp"
        )
        try:
            with os.fdopen(
                file_descriptor, "w", encoding="utf-8", newline="\n"
            ) as stream:
                yaml.safe_dump(
                    mapping, stream, sort_keys=False, allow_unicode=True
                )
                stream.flush()
                os.fsync(stream.fileno())
            try:
                os.link(temporary_name, destination)
            except FileExistsError as error:
                raise AtlasImportError(
                    "A private mapping already exists for this submission."
                ) from error
        finally:
            try:
                os.unlink(temporary_name)
            except FileNotFoundError:
                pass

    def load(self, fingerprint: str) -> dict | None:
        source = self.path_for(fingerprint)
        try:
            with source.open("r", encoding="utf-8") as stream:
                mapping = yaml.safe_load(stream)
        except FileNotFoundError:
            return None
        except (OSError, UnicodeError, yaml.YAMLError) as error:
            raise AtlasImportError(
                f"Private mapping could not be read safely: {error}."
            ) from error
        if not isinstance(mapping, dict):
            raise AtlasImportError("Private mapping must be a mapping.")
        if mapping.get("source", {}).get("fingerprint") != fingerprint:
            raise AtlasImportError("Private mapping fingerprint does not match.")
        return mapping

    def find_by_visit_id(self, visit_id: str) -> list[dict]:
        if not self.root.exists():
            return []
        mappings = []
        for source in sorted(self.root.glob("atlas-test-v1-*.private.yaml")):
            fingerprint = source.name.removeprefix(
                "atlas-test-v1-"
            ).removesuffix(".private.yaml")
            mapping = self.load(fingerprint)
            if (
                mapping is not None
                and mapping.get("generated", {}).get("visit_id") == visit_id
            ):
                mappings.append(mapping)
        return mappings

    def reserve(self, mapping: dict) -> None:
        fingerprint = mapping.get("source", {}).get("fingerprint")
        destination = self.path_for(fingerprint)
        self._write_new_atomic(destination, mapping)

    def complete(self, fingerprint: str) -> dict:
        mapping = self.load(fingerprint)
        if mapping is None:
            raise AtlasImportError("Private mapping reservation was not found.")
        if mapping.get("status") == "complete":
            return mapping
        if mapping.get("status") != "pending":
            raise AtlasImportError("Private mapping has an invalid status.")
        completed = deepcopy(mapping)
        completed["status"] = "complete"
        completed["completed_at"] = _timestamp(self.clock)
        self._write_atomic(self.path_for(fingerprint), completed)
        return completed

    def discard_pending(self, fingerprint: str, import_id: str) -> None:
        mapping = self.load(fingerprint)
        if mapping is None:
            return
        if (
            mapping.get("status") != "pending"
            or mapping.get("import_id") != import_id
        ):
            raise AtlasImportError(
                "Refusing to discard a private mapping not owned by this import."
            )
        try:
            self.path_for(fingerprint).unlink()
        except FileNotFoundError:
            pass
