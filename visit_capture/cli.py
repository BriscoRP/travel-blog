"""Maintainer command interface for the Visit Capture Foundation."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

import yaml

from .core import (
    EVIDENCE_TYPES,
    VisitError,
    YamlVisitStore,
    add_evidence,
    create_visit,
    validate_visit,
)
from .importer import AtlasImportError, YamlPrivateMappingStore, import_submission


def _ensure_outside_repository(path: Path, label: str) -> None:
    repository_root = Path(__file__).resolve().parent.parent
    resolved = path.expanduser().resolve()
    try:
        resolved.relative_to(repository_root)
    except ValueError:
        return
    raise AtlasImportError(
        f"{label} must be outside the public Project Atlas repository."
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="python -m visit_capture",
        description=(
            "Create and maintain private Open Visit records. "
            "This command never reads evidence files or publishes content."
        ),
    )
    parser.add_argument(
        "--store",
        required=True,
        type=Path,
        help="Explicit directory for private structured Visit records.",
    )
    commands = parser.add_subparsers(dest="command", required=True)

    create = commands.add_parser("create", help="Create one living Open Visit.")
    create.add_argument("--visit-id", required=True)
    create.add_argument("--place-id", required=True)
    create.add_argument("--visit-date", required=True)
    create.add_argument(
        "--date-precision", choices=("day", "month", "year"), required=True
    )
    create.add_argument(
        "--contributor-id",
        action="append",
        required=True,
        dest="contributor_ids",
        help="Opaque private contributor ID; repeat for multiple contributors.",
    )

    add = commands.add_parser(
        "add-evidence", help="Add one opaque evidence reference."
    )
    add.add_argument("--visit-id", required=True)
    add.add_argument("--evidence-id", required=True)
    add.add_argument("--type", choices=sorted(EVIDENCE_TYPES), required=True)
    add.add_argument("--captured-on")
    add.add_argument(
        "--description",
        help="Optional non-sensitive description; never enter a path, URL or contact.",
    )
    add.add_argument("--uncertain", action="store_true")

    show = commands.add_parser("show", help="Show one structured Visit record.")
    show.add_argument("--visit-id", required=True)

    validate = commands.add_parser("validate", help="Validate one Visit record.")
    validate.add_argument("--visit-id", required=True)

    importer = commands.add_parser(
        "import-csv",
        help="Import exactly one Atlas Test V1 CSV submission.",
    )
    importer.add_argument("--csv", required=True, type=Path)
    importer.add_argument(
        "--mapping-dir",
        required=True,
        type=Path,
        help="Private output directory for provenance and idempotency mappings.",
    )
    importer.add_argument(
        "--place-id",
        help="Existing opaque Place ID; omit to generate a new one.",
    )
    importer.add_argument(
        "--existing-visit-id",
        help=(
            "Explicit Open Visit to append this distinct submission to; "
            "omit to create a proposed new Visit."
        ),
    )
    importer.add_argument(
        "--media-type",
        action="append",
        choices=("photo", "video"),
        default=[],
        help=(
            "Type of each photo/video upload in source order; repeat once "
            "per uploaded item."
        ),
    )
    importer.add_argument(
        "--dry-run",
        action="store_true",
        help="Validate and preview without writing a Visit or private mapping.",
    )
    return parser


def main(arguments: list[str] | None = None) -> int:
    args = _parser().parse_args(arguments)
    store = YamlVisitStore(args.store)
    try:
        if args.command == "create":
            record = create_visit(
                store,
                visit_id=args.visit_id,
                place_id=args.place_id,
                visit_date=args.visit_date,
                visit_date_precision=args.date_precision,
                contributor_ids=args.contributor_ids,
            )
            print(f"Created Open Visit {record['visit_id']}.")
        elif args.command == "add-evidence":
            record = add_evidence(
                store,
                visit_id=args.visit_id,
                evidence_id=args.evidence_id,
                evidence_type=args.type,
                captured_on=args.captured_on,
                description=args.description,
                uncertain=args.uncertain,
            )
            print(
                f"Added {args.evidence_id} to Open Visit {record['visit_id']} "
                f"(record version {record['record_version']})."
            )
        elif args.command == "show":
            record = store.load(args.visit_id)
            print(yaml.safe_dump(record, sort_keys=False, allow_unicode=True), end="")
        elif args.command == "validate":
            record = store.load(args.visit_id)
            validate_visit(record)
            print(
                f"Visit {record['visit_id']} is valid, Open, and contains "
                f"{len(record['evidence'])} evidence reference(s)."
            )
        else:
            _ensure_outside_repository(args.store, "Visit store")
            _ensure_outside_repository(args.mapping_dir, "Private mapping directory")
            result = import_submission(
                args.csv,
                visit_store=store,
                mapping_store=YamlPrivateMappingStore(args.mapping_dir),
                place_id=args.place_id,
                existing_visit_id=args.existing_visit_id,
                media_types=tuple(args.media_type),
                dry_run=args.dry_run,
            )
            if args.dry_run:
                print(
                    yaml.safe_dump(
                        {
                            "dry_run": True,
                            "idempotent": result.idempotent,
                            "visit": result.visit,
                            "private_mapping": result.private_mapping,
                        },
                        sort_keys=False,
                        allow_unicode=True,
                    ),
                    end="",
                )
            else:
                outcome = "Already imported" if result.idempotent else "Imported"
                action = (
                    "appended to"
                    if result.private_mapping.get("operation") == "append"
                    else "created"
                )
                print(
                    f"{outcome} one Atlas Test V1 submission; {action} Open Visit "
                    f"{result.visit['visit_id']}."
                )
    except (VisitError, OSError, yaml.YAMLError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0
