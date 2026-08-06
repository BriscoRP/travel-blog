"""Tests for the Project Atlas Visit Capture Foundation."""

from datetime import datetime, timezone
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import tempfile
import unittest

import yaml

from visit_capture import (
    ConcurrentUpdateError,
    DuplicateEvidenceError,
    VisitAlreadyExistsError,
    VisitValidationError,
    YamlVisitStore,
    add_evidence,
    create_visit,
    validate_visit,
)
from visit_capture.cli import main as cli_main


VISIT_ID = "VIS-FICTION-0001"
PLACE_ID = "PLC-FICTION-0001"
CONTRIBUTOR_ID = "CTR-FICTION-0001"


def fixed_clock(hour: int):
    return lambda: datetime(2099, 4, 3, hour, 0, tzinfo=timezone.utc)


class VisitCaptureTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory(
            ignore_cleanup_errors=True
        )
        self.addCleanup(self.temporary_directory.cleanup)
        self.store = YamlVisitStore(self.temporary_directory.name)

    def create_fictional_visit(self):
        return create_visit(
            self.store,
            visit_id=VISIT_ID,
            place_id=PLACE_ID,
            visit_date="2099-04-03",
            visit_date_precision="day",
            contributor_ids=[CONTRIBUTOR_ID],
            clock=fixed_clock(10),
        )

    def test_create_visit_is_open_and_contains_no_evidence(self):
        record = self.create_fictional_visit()

        self.assertEqual(record["state"], "Open")
        self.assertEqual(record["record_version"], 1)
        self.assertEqual(record["evidence"], [])
        self.assertEqual(self.store.load(VISIT_ID), record)

    def test_create_does_not_overwrite_existing_visit(self):
        self.create_fictional_visit()

        with self.assertRaises(VisitAlreadyExistsError):
            self.create_fictional_visit()

    def test_evidence_can_be_added_over_time_without_replacing_earlier_items(self):
        self.create_fictional_visit()
        first = add_evidence(
            self.store,
            visit_id=VISIT_ID,
            evidence_id="EVD-FICTION-PHOTO-0001",
            evidence_type="photo",
            captured_on="2099-04-03",
            description="Fictional landscape reference.",
            clock=fixed_clock(11),
        )
        second = add_evidence(
            self.store,
            visit_id=VISIT_ID,
            evidence_id="EVD-FICTION-NOTE-0002",
            evidence_type="note",
            uncertain=True,
            clock=fixed_clock(12),
        )

        self.assertEqual(first["record_version"], 2)
        self.assertEqual(second["record_version"], 3)
        self.assertEqual(second["state"], "Open")
        self.assertEqual(
            [item["evidence_id"] for item in second["evidence"]],
            ["EVD-FICTION-PHOTO-0001", "EVD-FICTION-NOTE-0002"],
        )

    def test_duplicate_evidence_id_is_rejected_without_changing_record(self):
        self.create_fictional_visit()
        add_evidence(
            self.store,
            visit_id=VISIT_ID,
            evidence_id="EVD-FICTION-AUDIO-0001",
            evidence_type="audio",
            clock=fixed_clock(11),
        )
        before = self.store.load(VISIT_ID)

        with self.assertRaises(DuplicateEvidenceError):
            add_evidence(
                self.store,
                visit_id=VISIT_ID,
                evidence_id="EVD-FICTION-AUDIO-0001",
                evidence_type="audio",
                clock=fixed_clock(12),
            )

        self.assertEqual(self.store.load(VISIT_ID), before)

    def test_invalid_evidence_is_rejected_without_changing_record(self):
        self.create_fictional_visit()
        before = self.store.load(VISIT_ID)

        with self.assertRaises(VisitValidationError):
            add_evidence(
                self.store,
                visit_id=VISIT_ID,
                evidence_id="EVD-FICTION-0001",
                evidence_type="document",
                clock=fixed_clock(11),
            )

        self.assertEqual(self.store.load(VISIT_ID), before)

    def test_private_storage_reference_is_rejected_without_changing_record(self):
        self.create_fictional_visit()
        before = self.store.load(VISIT_ID)

        with self.assertRaises(VisitValidationError):
            add_evidence(
                self.store,
                visit_id=VISIT_ID,
                evidence_id="EVD-FICTION-PHOTO-0001",
                evidence_type="photo",
                description="Stored at https://private.invalid/evidence",
                clock=fixed_clock(11),
            )

        self.assertEqual(self.store.load(VISIT_ID), before)

    def test_unknown_state_is_rejected(self):
        record = self.create_fictional_visit()
        record["state"] = "Published"

        with self.assertRaises(VisitValidationError):
            validate_visit(record)

    def test_missing_required_field_is_rejected(self):
        record = self.create_fictional_visit()
        del record["visit_date"]

        with self.assertRaises(VisitValidationError):
            validate_visit(record)

    def test_invalid_calendar_date_is_rejected(self):
        with self.assertRaises(VisitValidationError):
            create_visit(
                self.store,
                visit_id=VISIT_ID,
                place_id=PLACE_ID,
                visit_date="2099-02-30",
                visit_date_precision="day",
                contributor_ids=[CONTRIBUTOR_ID],
                clock=fixed_clock(10),
            )

    def test_stale_save_is_rejected(self):
        original = self.create_fictional_visit()
        add_evidence(
            self.store,
            visit_id=VISIT_ID,
            evidence_id="EVD-FICTION-VIDEO-0001",
            evidence_type="video",
            clock=fixed_clock(11),
        )
        original["record_version"] = 2
        original["last_modified_at"] = "2099-04-03T12:00:00Z"

        with self.assertRaises(ConcurrentUpdateError):
            self.store.save(original, expected_record_version=1)

    def test_yaml_contains_only_structured_opaque_references(self):
        self.create_fictional_visit()
        add_evidence(
            self.store,
            visit_id=VISIT_ID,
            evidence_id="EVD-FICTION-PHOTO-0001",
            evidence_type="photo",
            clock=fixed_clock(11),
        )
        record_path = Path(self.temporary_directory.name) / f"{VISIT_ID}.yaml"
        content = record_path.read_text(encoding="utf-8")
        parsed = yaml.safe_load(content)

        self.assertNotIn("http", content)
        self.assertNotIn("\\", content)
        self.assertNotIn("/", content)
        self.assertNotIn("filename", content.lower())
        self.assertEqual(parsed["contributor_ids"], [CONTRIBUTOR_ID])
        self.assertEqual(
            parsed["evidence"][0]["evidence_id"], "EVD-FICTION-PHOTO-0001"
        )

    def test_cli_creates_updates_and_validates_one_living_visit(self):
        store_path = self.temporary_directory.name
        output = StringIO()

        with redirect_stdout(output):
            create_result = cli_main(
                [
                    "--store",
                    store_path,
                    "create",
                    "--visit-id",
                    VISIT_ID,
                    "--place-id",
                    PLACE_ID,
                    "--visit-date",
                    "2099-04",
                    "--date-precision",
                    "month",
                    "--contributor-id",
                    CONTRIBUTOR_ID,
                ]
            )
            add_result = cli_main(
                [
                    "--store",
                    store_path,
                    "add-evidence",
                    "--visit-id",
                    VISIT_ID,
                    "--evidence-id",
                    "EVD-FICTION-PHOTO-0001",
                    "--type",
                    "photo",
                ]
            )
            validate_result = cli_main(
                [
                    "--store",
                    store_path,
                    "validate",
                    "--visit-id",
                    VISIT_ID,
                ]
            )

        self.assertEqual((create_result, add_result, validate_result), (0, 0, 0))
        self.assertIn("Created Open Visit", output.getvalue())
        self.assertIn("contains 1 evidence reference(s)", output.getvalue())
        self.assertEqual(self.store.load(VISIT_ID)["state"], "Open")


if __name__ == "__main__":
    unittest.main()
