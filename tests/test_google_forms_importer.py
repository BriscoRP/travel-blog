"""Tests for the one-submission Atlas Test V1 CSV importer."""

from contextlib import redirect_stderr, redirect_stdout
from copy import deepcopy
from datetime import datetime, timezone
from io import StringIO
from pathlib import Path
import tempfile
import unittest

import yaml

from visit_capture import YamlVisitStore
from visit_capture import (
    ConcurrentUpdateError,
    VisitValidationError,
    add_evidence,
)
from visit_capture.cli import main as cli_main
from visit_capture.importer import (
    AtlasImportError,
    LEGACY_VISITORS_COLUMN,
    VISITORS_COLUMN,
    YamlPrivateMappingStore,
    import_submission,
    read_single_submission,
)


FIXTURE = (
    Path(__file__).parent / "fixtures" / "atlas-test-v1-fictional.csv"
)
LATER_FIXTURE = (
    Path(__file__).parent
    / "fixtures"
    / "atlas-test-v1-fictional-later.csv"
)
EXISTING_PLACE_ID = "PLC-FICTION-EXISTING"


class DeterministicIds:
    def __init__(self):
        self.counts = {}

    def __call__(self, prefix):
        self.counts[prefix] = self.counts.get(prefix, 0) + 1
        return f"{prefix}-FICTION-{self.counts[prefix]:04d}"


def fixed_clock():
    return datetime(2099, 4, 4, 10, 30, tzinfo=timezone.utc)


class FailingVisitStore:
    def create(self, record):
        raise OSError("Fictional storage failure.")

    def load(self, visit_id):
        raise AssertionError("load should not be called")

    def save(self, record, expected_record_version):
        raise AssertionError("save should not be called")


class StaticVisitStore:
    def __init__(self, record):
        self.record = record

    def create(self, record):
        raise AssertionError("create should not be called")

    def load(self, visit_id):
        return deepcopy(self.record)

    def save(self, record, expected_record_version):
        raise AssertionError("save should not be called")


class FailingSaveStore:
    def __init__(self, delegate):
        self.delegate = delegate

    def create(self, record):
        return self.delegate.create(record)

    def load(self, visit_id):
        return self.delegate.load(visit_id)

    def save(self, record, expected_record_version):
        raise OSError("Fictional append storage failure.")


class StaleOnSaveStore:
    def __init__(self, delegate):
        self.delegate = delegate

    def create(self, record):
        return self.delegate.create(record)

    def load(self, visit_id):
        return self.delegate.load(visit_id)

    def save(self, record, expected_record_version):
        add_evidence(
            self.delegate,
            visit_id=record["visit_id"],
            evidence_id="EVD-FICTION-CONCURRENT-0001",
            evidence_type="note",
            description="Fictional concurrent evidence.",
            clock=lambda: datetime(
                2099, 4, 4, 11, 0, tzinfo=timezone.utc
            ),
        )
        return self.delegate.save(record, expected_record_version)


class GoogleFormsImporterTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory(
            ignore_cleanup_errors=True
        )
        self.addCleanup(self.temporary_directory.cleanup)
        root = Path(self.temporary_directory.name)
        self.visit_root = root / "visits"
        self.mapping_root = root / "mappings"
        self.visit_store = YamlVisitStore(self.visit_root)
        self.mapping_store = YamlPrivateMappingStore(
            self.mapping_root, clock=fixed_clock
        )
        self.ids = DeterministicIds()

    def import_fictional_submission(self, **overrides):
        arguments = {
            "visit_store": self.visit_store,
            "mapping_store": self.mapping_store,
            "media_types": ("photo",),
            "id_factory": self.ids,
            "clock": fixed_clock,
        }
        arguments.update(overrides)
        return import_submission(FIXTURE, **arguments)

    def append_fictional_submission(self, visit_id, **overrides):
        arguments = {
            "visit_store": self.visit_store,
            "mapping_store": self.mapping_store,
            "existing_visit_id": visit_id,
            "media_types": (),
            "id_factory": self.ids,
            "clock": fixed_clock,
        }
        arguments.update(overrides)
        return import_submission(LATER_FIXTURE, **arguments)

    def test_legacy_visitor_heading_is_accepted_and_preserved(self):
        submission = read_single_submission(FIXTURE)

        self.assertEqual(submission.visitors_heading, LEGACY_VISITORS_COLUMN)
        self.assertIn(LEGACY_VISITORS_COLUMN, submission.values)
        self.assertNotIn(VISITORS_COLUMN, submission.values)
        self.assertEqual(
            submission.contributor_labels,
            ("Contributor Alpha", "Contributor Beta"),
        )

    def test_correct_visitor_heading_is_also_accepted(self):
        corrected_csv = Path(self.temporary_directory.name) / "corrected.csv"
        content = FIXTURE.read_text(encoding="utf-8").replace(
            LEGACY_VISITORS_COLUMN, VISITORS_COLUMN, 1
        )
        corrected_csv.write_text(content, encoding="utf-8")

        submission = read_single_submission(corrected_csv)

        self.assertEqual(submission.visitors_heading, VISITORS_COLUMN)
        self.assertIn(VISITORS_COLUMN, submission.values)
        self.assertNotIn(LEGACY_VISITORS_COLUMN, submission.values)

    def test_utf8_bom_is_accepted(self):
        bom_csv = Path(self.temporary_directory.name) / "bom.csv"
        bom_csv.write_bytes(b"\xef\xbb\xbf" + FIXTURE.read_bytes())

        submission = read_single_submission(bom_csv)

        self.assertEqual(
            submission.values["What place did you visit?"], "Example Meadow"
        )

    def test_unknown_and_duplicate_headings_are_rejected(self):
        original = FIXTURE.read_text(encoding="utf-8").rstrip("\n")
        header, row = original.split("\n", 1)
        cases = {
            "unknown": f"{header},Unexpected private field\n{row},value\n",
            "duplicate": (
                f"{header},What place did you visit?\n"
                f"{row},Duplicate Example Meadow\n"
            ),
        }
        for name, content in cases.items():
            with self.subTest(name=name):
                csv_path = Path(self.temporary_directory.name) / f"{name}.csv"
                csv_path.write_text(content, encoding="utf-8")
                with self.assertRaises(AtlasImportError):
                    read_single_submission(csv_path)

    def test_dry_run_returns_preview_without_writing(self):
        result = self.import_fictional_submission(dry_run=True)

        self.assertTrue(result.dry_run)
        self.assertFalse(result.idempotent)
        self.assertEqual(result.visit["state"], "Open")
        self.assertEqual(result.visit["visit_date"], "2099-04-03")
        self.assertEqual(result.private_mapping["status"], "dry-run")
        self.assertFalse(self.visit_root.exists())
        self.assertFalse(self.mapping_root.exists())

    def test_import_creates_one_complete_open_visit_and_private_mapping(self):
        result = self.import_fictional_submission()
        stored = self.visit_store.load(result.visit["visit_id"])
        mapping = yaml.safe_load(
            result.mapping_path.read_text(encoding="utf-8")
        )

        self.assertEqual(stored["state"], "Open")
        self.assertEqual(stored["record_version"], 1)
        self.assertEqual(
            [item["evidence_type"] for item in stored["evidence"]],
            ["note", "photo"],
        )
        self.assertEqual(mapping["status"], "complete")
        self.assertEqual(
            mapping["source"]["visitors_heading"], LEGACY_VISITORS_COLUMN
        )
        self.assertEqual(
            mapping["generated"]["place"]["private_name"], "Example Meadow"
        )

        public_record = yaml.safe_dump(stored)
        self.assertNotIn("Contributor Alpha", public_record)
        self.assertNotIn("drive.example.invalid", public_record)
        private_output = yaml.safe_dump(mapping)
        self.assertIn("Contributor Alpha", private_output)
        self.assertIn("drive.example.invalid", private_output)

    def test_reimport_is_idempotent(self):
        first = self.import_fictional_submission()
        second = self.import_fictional_submission(
            id_factory=DeterministicIds()
        )

        self.assertTrue(second.idempotent)
        self.assertEqual(second.visit, first.visit)
        self.assertEqual(second.private_mapping, first.private_mapping)
        self.assertEqual(len(list(self.visit_root.glob("*.yaml"))), 1)
        self.assertEqual(
            len(list(self.mapping_root.glob("*.private.yaml"))), 1
        )

    def test_later_submission_appends_only_with_explicit_visit_id(self):
        first = self.import_fictional_submission()

        appended = self.append_fictional_submission(first.visit["visit_id"])

        self.assertFalse(appended.idempotent)
        self.assertEqual(appended.visit["visit_id"], first.visit["visit_id"])
        self.assertEqual(appended.visit["record_version"], 2)
        self.assertEqual(
            [item["evidence_type"] for item in appended.visit["evidence"]],
            ["note", "photo", "note", "audio"],
        )
        self.assertEqual(appended.private_mapping["operation"], "append")
        self.assertEqual(appended.private_mapping["base_record_version"], 1)

    def test_append_preserves_all_earlier_evidence(self):
        first = self.import_fictional_submission()
        earlier = deepcopy(first.visit["evidence"])

        appended = self.append_fictional_submission(first.visit["visit_id"])

        self.assertEqual(appended.visit["evidence"][: len(earlier)], earlier)

    def test_reimporting_later_submission_is_idempotent(self):
        first = self.import_fictional_submission()
        appended = self.append_fictional_submission(first.visit["visit_id"])

        repeated = self.append_fictional_submission(
            first.visit["visit_id"], id_factory=DeterministicIds()
        )

        self.assertTrue(repeated.idempotent)
        self.assertEqual(repeated.visit, appended.visit)
        self.assertEqual(repeated.visit["record_version"], 2)
        self.assertEqual(len(repeated.visit["evidence"]), 4)
        self.assertEqual(len(list(self.mapping_root.glob("*.yaml"))), 2)

    def test_reimporting_initial_submission_after_append_is_idempotent(self):
        first = self.import_fictional_submission()
        appended = self.append_fictional_submission(first.visit["visit_id"])

        repeated = self.import_fictional_submission(
            id_factory=DeterministicIds()
        )

        self.assertTrue(repeated.idempotent)
        self.assertEqual(repeated.visit, appended.visit)
        self.assertEqual(len(repeated.visit["evidence"]), 4)

    def test_omitting_existing_visit_id_creates_no_accidental_merge(self):
        first = self.import_fictional_submission()

        separate = import_submission(
            LATER_FIXTURE,
            visit_store=self.visit_store,
            mapping_store=self.mapping_store,
            media_types=(),
            id_factory=self.ids,
            clock=fixed_clock,
        )

        self.assertNotEqual(separate.visit["visit_id"], first.visit["visit_id"])
        self.assertNotEqual(separate.visit["place_id"], first.visit["place_id"])
        self.assertEqual(len(list(self.visit_root.glob("*.yaml"))), 2)

    def test_append_dry_run_does_not_change_visit_or_write_mapping(self):
        first = self.import_fictional_submission()
        before = self.visit_store.load(first.visit["visit_id"])

        preview = self.append_fictional_submission(
            first.visit["visit_id"], dry_run=True
        )

        self.assertTrue(preview.dry_run)
        self.assertEqual(preview.visit["record_version"], 2)
        self.assertEqual(preview.private_mapping["status"], "dry-run")
        self.assertEqual(self.visit_store.load(first.visit["visit_id"]), before)
        self.assertEqual(len(list(self.mapping_root.glob("*.yaml"))), 1)

    def test_closed_or_unknown_visit_states_reject_append(self):
        first = self.import_fictional_submission()

        for state in ("Published", "Unexpected"):
            with self.subTest(state=state):
                invalid = deepcopy(first.visit)
                invalid["state"] = state
                with self.assertRaises(VisitValidationError):
                    self.append_fictional_submission(
                        first.visit["visit_id"],
                        visit_store=StaticVisitStore(invalid),
                    )

    def test_conflicting_submitted_place_is_reported(self):
        first = self.import_fictional_submission()
        conflicting = Path(self.temporary_directory.name) / "place-conflict.csv"
        conflicting.write_text(
            LATER_FIXTURE.read_text(encoding="utf-8").replace(
                "Example Meadow", "Different Fictional Place", 1
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            AtlasImportError, "place name was.*submitted"
        ):
            import_submission(
                conflicting,
                visit_store=self.visit_store,
                mapping_store=self.mapping_store,
                existing_visit_id=first.visit["visit_id"],
                media_types=(),
                id_factory=self.ids,
                clock=fixed_clock,
            )

    def test_conflicting_submitted_visitors_are_reported(self):
        first = self.import_fictional_submission()
        conflicting = (
            Path(self.temporary_directory.name) / "visitor-conflict.csv"
        )
        conflicting.write_text(
            LATER_FIXTURE.read_text(encoding="utf-8").replace(
                "Contributor Alpha, Contributor Beta",
                "Contributor Alpha, Contributor Gamma",
                1,
            ),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            AtlasImportError, "visitor set was.*submitted"
        ):
            import_submission(
                conflicting,
                visit_store=self.visit_store,
                mapping_store=self.mapping_store,
                existing_visit_id=first.visit["visit_id"],
                media_types=(),
                id_factory=self.ids,
                clock=fixed_clock,
            )

    def test_all_submitted_identity_differences_are_reported_together(self):
        first = self.import_fictional_submission()
        conflicting = Path(self.temporary_directory.name) / "differences.csv"
        content = LATER_FIXTURE.read_text(encoding="utf-8")
        content = content.replace(
            "Sampleton, Testshire, TE1 2ST",
            "Elsewhere, Testshire, TE9 9ZZ",
            1,
        )
        content = content.replace("03/04/2099", "04/04/2099", 1)
        conflicting.write_text(content, encoding="utf-8")

        with self.assertRaises(AtlasImportError) as context:
            import_submission(
                conflicting,
                visit_store=self.visit_store,
                mapping_store=self.mapping_store,
                existing_visit_id=first.visit["visit_id"],
                media_types=(),
                id_factory=self.ids,
                clock=fixed_clock,
            )

        message = str(context.exception)
        self.assertIn("location was", message)
        self.assertIn("Visit date was", message)

    def test_conflicting_private_contributor_mapping_is_rejected(self):
        first = self.import_fictional_submission()
        create_mapping_path = next(
            self.mapping_root.glob("*.private.yaml")
        )
        mapping = yaml.safe_load(
            create_mapping_path.read_text(encoding="utf-8")
        )
        mapping["generated"]["contributors"][0][
            "contributor_id"
        ] = "CTR-FICTION-CONFLICT-0001"
        create_mapping_path.write_text(
            yaml.safe_dump(mapping, sort_keys=False),
            encoding="utf-8",
        )

        with self.assertRaisesRegex(
            AtlasImportError, "contributor mapping conflicts"
        ):
            self.append_fictional_submission(first.visit["visit_id"])

    def test_conflicting_place_override_is_rejected(self):
        first = self.import_fictional_submission()

        with self.assertRaisesRegex(AtlasImportError, "Supplied Place ID"):
            self.append_fictional_submission(
                first.visit["visit_id"],
                place_id="PLC-FICTION-DIFFERENT",
            )

    def test_stale_record_version_fails_without_new_mapping(self):
        first = self.import_fictional_submission()

        with self.assertRaises(ConcurrentUpdateError):
            self.append_fictional_submission(
                first.visit["visit_id"],
                visit_store=StaleOnSaveStore(self.visit_store),
            )

        current = self.visit_store.load(first.visit["visit_id"])
        self.assertEqual(current["record_version"], 2)
        self.assertEqual(current["evidence"][-1]["evidence_id"], "EVD-FICTION-CONCURRENT-0001")
        self.assertEqual(len(list(self.mapping_root.glob("*.yaml"))), 1)

    def test_append_storage_failure_leaves_visit_and_mapping_consistent(self):
        first = self.import_fictional_submission()
        before = self.visit_store.load(first.visit["visit_id"])

        with self.assertRaises(OSError):
            self.append_fictional_submission(
                first.visit["visit_id"],
                visit_store=FailingSaveStore(self.visit_store),
            )

        self.assertEqual(self.visit_store.load(first.visit["visit_id"]), before)
        self.assertEqual(len(list(self.mapping_root.glob("*.yaml"))), 1)

    def test_later_csv_column_order_multiline_and_commas_are_preserved(self):
        submission = read_single_submission(LATER_FIXTURE)

        self.assertEqual(submission.visitors_heading, VISITORS_COLUMN)
        self.assertEqual(submission.headings[-1], VISITORS_COLUMN)
        self.assertIn("bench, beside", submission.values["Tell us about your visit"])
        self.assertIn("\n", submission.values["Tell us about your visit"])

    def test_multiple_uploaded_links_are_registered_separately(self):
        multiple = Path(self.temporary_directory.name) / "multiple-media.csv"
        multiple.write_text(
            FIXTURE.read_text(encoding="utf-8").replace(
                "https://drive.example.invalid/photo-reference,",
                '"https://drive.example.invalid/photo-one, '
                'https://drive.example.invalid/video-two",',
                1,
            ),
            encoding="utf-8",
        )

        result = import_submission(
            multiple,
            visit_store=self.visit_store,
            mapping_store=self.mapping_store,
            media_types=("photo", "video"),
            id_factory=self.ids,
            clock=fixed_clock,
        )

        self.assertEqual(
            [item["evidence_type"] for item in result.visit["evidence"]],
            ["note", "photo", "video"],
        )
        provider_references = [
            item["provider_reference"]
            for item in result.private_mapping["generated"]["evidence"]
            if item["provider_reference"] is not None
        ]
        self.assertEqual(len(provider_references), 2)

    def test_pending_mapping_recovers_after_visit_was_created(self):
        preview = self.import_fictional_submission(dry_run=True)
        pending = deepcopy(preview.private_mapping)
        pending["status"] = "pending"
        self.mapping_store.reserve(pending)
        self.visit_store.create(preview.visit)

        recovered = self.import_fictional_submission(
            id_factory=DeterministicIds()
        )

        self.assertTrue(recovered.idempotent)
        self.assertEqual(recovered.visit, preview.visit)
        self.assertEqual(recovered.private_mapping["status"], "complete")

    def test_pending_append_recovers_after_visit_was_updated(self):
        first = self.import_fictional_submission()
        preview = self.append_fictional_submission(
            first.visit["visit_id"], dry_run=True
        )
        pending = deepcopy(preview.private_mapping)
        pending["status"] = "pending"
        self.mapping_store.reserve(pending)
        self.visit_store.save(
            preview.visit,
            expected_record_version=pending["base_record_version"],
        )

        recovered = self.append_fictional_submission(
            first.visit["visit_id"], id_factory=DeterministicIds()
        )

        self.assertTrue(recovered.idempotent)
        self.assertEqual(recovered.visit, preview.visit)
        self.assertEqual(recovered.private_mapping["status"], "complete")

    def test_reimport_rejects_a_conflicting_place_override(self):
        self.import_fictional_submission()

        with self.assertRaises(AtlasImportError):
            self.import_fictional_submission(
                place_id="PLC-FICTION-DIFFERENT",
                id_factory=DeterministicIds(),
            )

    def test_existing_place_id_is_used_without_generating_a_place(self):
        result = self.import_fictional_submission(place_id=EXISTING_PLACE_ID)

        self.assertEqual(result.visit["place_id"], EXISTING_PLACE_ID)
        self.assertFalse(
            result.private_mapping["generated"]["place"]["generated"]
        )

    def test_ambiguous_uploaded_media_type_fails_before_writing(self):
        with self.assertRaises(AtlasImportError):
            self.import_fictional_submission(media_types=())

        self.assertFalse(self.visit_root.exists())
        self.assertFalse(self.mapping_root.exists())

    def test_visit_storage_failure_discards_new_pending_mapping(self):
        with self.assertRaises(OSError):
            import_submission(
                FIXTURE,
                visit_store=FailingVisitStore(),
                mapping_store=self.mapping_store,
                media_types=("photo",),
                id_factory=DeterministicIds(),
                clock=fixed_clock,
            )

        self.assertEqual(list(self.mapping_root.glob("*.yaml")), [])

    def test_multiple_rows_are_rejected(self):
        duplicate_csv = Path(self.temporary_directory.name) / "duplicate.csv"
        original = FIXTURE.read_text(encoding="utf-8")
        header, row = original.rstrip("\n").split("\n", 1)
        duplicate_csv.write_text(
            f"{header}\n{row}\n{row}\n", encoding="utf-8"
        )

        with self.assertRaises(AtlasImportError):
            read_single_submission(duplicate_csv)

    def test_cli_dry_run_prints_preview_and_writes_nothing(self):
        output = StringIO()
        errors = StringIO()

        with redirect_stdout(output), redirect_stderr(errors):
            result = cli_main(
                [
                    "--store",
                    str(self.visit_root),
                    "import-csv",
                    "--csv",
                    str(FIXTURE),
                    "--mapping-dir",
                    str(self.mapping_root),
                    "--media-type",
                    "photo",
                    "--dry-run",
                ]
            )

        self.assertEqual(result, 0, errors.getvalue())
        preview = yaml.safe_load(output.getvalue())
        self.assertTrue(preview["dry_run"])
        self.assertEqual(preview["visit"]["state"], "Open")
        self.assertEqual(preview["private_mapping"]["status"], "dry-run")
        self.assertFalse(self.visit_root.exists())
        self.assertFalse(self.mapping_root.exists())

    def test_cli_rejects_private_output_inside_public_repository(self):
        output = StringIO()
        errors = StringIO()
        repository_private_path = Path(__file__).parent / "must-not-be-created"

        with redirect_stdout(output), redirect_stderr(errors):
            result = cli_main(
                [
                    "--store",
                    str(repository_private_path),
                    "import-csv",
                    "--csv",
                    str(FIXTURE),
                    "--mapping-dir",
                    str(self.mapping_root),
                    "--media-type",
                    "photo",
                    "--dry-run",
                ]
            )

        self.assertEqual(result, 1)
        self.assertIn("outside the public Project Atlas repository", errors.getvalue())
        self.assertFalse(repository_private_path.exists())

    def test_cli_explicitly_appends_later_submission(self):
        output = StringIO()
        errors = StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            first_result = cli_main(
                [
                    "--store",
                    str(self.visit_root),
                    "import-csv",
                    "--csv",
                    str(FIXTURE),
                    "--mapping-dir",
                    str(self.mapping_root),
                    "--media-type",
                    "photo",
                ]
            )
        self.assertEqual(first_result, 0, errors.getvalue())
        visit_path = next(self.visit_root.glob("VIS-*.yaml"))
        visit_id = visit_path.stem

        output = StringIO()
        errors = StringIO()
        with redirect_stdout(output), redirect_stderr(errors):
            append_result = cli_main(
                [
                    "--store",
                    str(self.visit_root),
                    "import-csv",
                    "--csv",
                    str(LATER_FIXTURE),
                    "--mapping-dir",
                    str(self.mapping_root),
                    "--existing-visit-id",
                    visit_id,
                ]
            )

        self.assertEqual(append_result, 0, errors.getvalue())
        self.assertIn("appended to Open Visit", output.getvalue())
        visit = self.visit_store.load(visit_id)
        self.assertEqual(visit["record_version"], 2)
        self.assertEqual(len(visit["evidence"]), 4)


if __name__ == "__main__":
    unittest.main()
