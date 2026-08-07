"""Fictional tests for Google response discovery and importer bridging."""

from copy import deepcopy
from pathlib import Path
import tempfile
import unittest

from visit_capture import YamlVisitStore
from visit_capture.google_bridge import (
    PrivateResponseStateStore,
    discover_responses,
    import_selected_response,
)
from visit_capture.google_sheets import SheetResponseBatch
from visit_capture.importer import (
    ADVICE_COLUMN,
    ACCESSIBILITY_COLUMN,
    AUDIO_COLUMN,
    AtlasImportError,
    EXPERIENCE_COLUMN,
    LEGACY_VISITORS_COLUMN,
    LOCATION_COLUMN,
    MEDIA_COLUMN,
    PARKING_COLUMN,
    PLACE_COLUMN,
    RECOMMEND_COLUMN,
    TIMESTAMP_COLUMN,
    TOILETS_COLUMN,
    VISITORS_COLUMN,
    VISIT_DATE_COLUMN,
    YamlPrivateMappingStore,
)


HEADINGS = (
    TIMESTAMP_COLUMN,
    PLACE_COLUMN,
    LOCATION_COLUMN,
    LEGACY_VISITORS_COLUMN,
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


def fictional_values(number: int, **overrides) -> dict[str, str]:
    values = {
        TIMESTAMP_COLUMN: f"{number:02d}/05/2099 10:00:00",
        PLACE_COLUMN: f"Fictional Place {number}",
        LOCATION_COLUMN: f"Example District {number}, Testshire, TE{number} 1AA",
        LEGACY_VISITORS_COLUMN: "Contributor Alpha, Contributor Beta",
        VISITORS_COLUMN: "Contributor Alpha, Contributor Beta",
        VISIT_DATE_COLUMN: f"{number:02d}/05/2099",
        EXPERIENCE_COLUMN: f"Fictional memory {number}.",
        ADVICE_COLUMN: "",
        PARKING_COLUMN: "Did not look",
        TOILETS_COLUMN: "Did not look",
        ACCESSIBILITY_COLUMN: "",
        RECOMMEND_COLUMN: "Yes",
        MEDIA_COLUMN: "",
        AUDIO_COLUMN: "",
    }
    values.update(overrides)
    return values


def fictional_row(
    number: int,
    *,
    headings: tuple[str, ...] = HEADINGS,
    **overrides,
) -> tuple[str, ...]:
    values = fictional_values(number, **overrides)
    return tuple(values[heading] for heading in headings)


class FakeGoogleSource:
    def __init__(self, rows, headings=HEADINGS):
        self.batch = SheetResponseBatch(
            headings=tuple(headings),
            rows=tuple(tuple(row) for row in rows),
        )

    def fetch(self):
        return deepcopy(self.batch)


class FailingGoogleSource:
    def fetch(self):
        raise AtlasImportError("Fictional Google network failure.")


class FailingVisitStore:
    def create(self, record):
        raise OSError("Fictional Visit write failure.")

    def load(self, visit_id):
        raise AssertionError("load should not be called")

    def save(self, record, expected_record_version):
        raise AssertionError("save should not be called")


class GoogleBridgeTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory(
            ignore_cleanup_errors=True
        )
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        self.state_store = PrivateResponseStateStore(
            self.root / "google" / "response-state.yaml"
        )
        self.visit_store = YamlVisitStore(self.root / "visits")
        self.mapping_store = YamlPrivateMappingStore(self.root / "mappings")

    def discover(self, source):
        return discover_responses(source, self.state_store)

    def import_response(self, source, response_id, **overrides):
        arguments = {
            "state_store": self.state_store,
            "response_id": response_id,
            "visit_store": self.visit_store,
            "mapping_store": self.mapping_store,
        }
        arguments.update(overrides)
        return import_selected_response(source, **arguments)

    def test_discovers_twelve_fictional_responses_as_opaque_pending_ids(self):
        source = FakeGoogleSource(
            [fictional_row(number) for number in range(1, 13)]
        )

        result = self.discover(source)

        self.assertEqual(result.total_count, 12)
        self.assertEqual(result.pending_count, 12)
        self.assertEqual(result.processed_count, 0)
        self.assertEqual(len(set(result.pending_ids)), 12)
        self.assertTrue(all(value.startswith("RSP-") for value in result.pending_ids))
        self.assertNotIn("Fictional Place", " ".join(result.pending_ids))

    def test_repeated_discovery_does_not_duplicate_responses(self):
        source = FakeGoogleSource([fictional_row(1), fictional_row(2)])
        first = self.discover(source)

        second = self.discover(source)

        self.assertEqual(second.pending_ids, first.pending_ids)
        self.assertEqual(second.total_count, 2)

    def test_dry_run_leaves_selected_response_pending_and_writes_nothing(self):
        source = FakeGoogleSource([fictional_row(1)])
        response_id = self.discover(source).pending_ids[0]

        result = self.import_response(source, response_id, dry_run=True)

        self.assertTrue(result.dry_run)
        self.assertEqual(result.visit["state"], "Open")
        self.assertEqual(self.discover(source).pending_count, 1)
        self.assertFalse((self.root / "visits").exists())
        self.assertFalse((self.root / "mappings").exists())

    def test_persisted_import_marks_processed_and_creates_one_visit(self):
        source = FakeGoogleSource([fictional_row(1)])
        response_id = self.discover(source).pending_ids[0]

        result = self.import_response(source, response_id)

        discovery = self.discover(source)
        self.assertEqual(discovery.processed_count, 1)
        self.assertEqual(discovery.pending_count, 0)
        self.assertEqual(len(list((self.root / "visits").glob("*.yaml"))), 1)
        self.assertEqual(self.visit_store.load(result.visit["visit_id"]), result.visit)

    def test_retrieving_processed_response_is_idempotent(self):
        source = FakeGoogleSource([fictional_row(1)])
        response_id = self.discover(source).pending_ids[0]
        first = self.import_response(source, response_id)

        second = self.import_response(source, response_id)

        self.assertTrue(second.idempotent)
        self.assertEqual(second.visit, first.visit)
        self.assertEqual(len(list((self.root / "visits").glob("*.yaml"))), 1)

    def test_similar_submissions_are_never_automatically_merged(self):
        shared = {
            PLACE_COLUMN: "Fictional Similar Place",
            LOCATION_COLUMN: "Example Town, Testshire, TE1 1AA",
            VISIT_DATE_COLUMN: "01/05/2099",
        }
        source = FakeGoogleSource(
            [
                fictional_row(1, **shared),
                fictional_row(2, **shared),
            ]
        )
        pending = self.discover(source).pending_ids

        first = self.import_response(source, pending[0])
        second = self.import_response(source, pending[1])

        self.assertNotEqual(first.visit["visit_id"], second.visit["visit_id"])
        self.assertNotEqual(first.visit["place_id"], second.visit["place_id"])
        self.assertEqual(len(list((self.root / "visits").glob("*.yaml"))), 2)

    def test_identical_distinct_rows_are_not_mistaken_for_a_retry(self):
        identical = fictional_row(1)
        source = FakeGoogleSource([identical, identical])
        pending = self.discover(source).pending_ids

        first = self.import_response(source, pending[0])
        second = self.import_response(source, pending[1])

        self.assertNotEqual(first.visit["visit_id"], second.visit["visit_id"])
        self.assertEqual(len(list((self.root / "visits").glob("*.yaml"))), 2)

    def test_later_submission_appends_only_to_explicit_visit_id(self):
        shared = {
            PLACE_COLUMN: "Fictional Living Visit",
            LOCATION_COLUMN: "Example Town, Testshire, TE1 1AA",
            VISIT_DATE_COLUMN: "01/05/2099",
        }
        source = FakeGoogleSource(
            [
                fictional_row(1, **shared),
                fictional_row(
                    2,
                    **shared,
                    **{EXPERIENCE_COLUMN: "A later fictional memory."},
                ),
            ]
        )
        pending = self.discover(source).pending_ids
        first = self.import_response(source, pending[0])
        earlier_evidence = deepcopy(first.visit["evidence"])

        appended = self.import_response(
            source,
            pending[1],
            existing_visit_id=first.visit["visit_id"],
        )

        self.assertEqual(appended.visit["visit_id"], first.visit["visit_id"])
        self.assertEqual(appended.visit["record_version"], 2)
        self.assertEqual(appended.visit["evidence"][:1], earlier_evidence)
        self.assertEqual(len(list((self.root / "visits").glob("*.yaml"))), 1)

    def test_later_submission_without_visit_id_creates_separate_visit(self):
        shared = {
            PLACE_COLUMN: "Fictional Living Visit",
            LOCATION_COLUMN: "Example Town, Testshire, TE1 1AA",
            VISIT_DATE_COLUMN: "01/05/2099",
        }
        source = FakeGoogleSource(
            [fictional_row(1, **shared), fictional_row(2, **shared)]
        )
        pending = self.discover(source).pending_ids
        first = self.import_response(source, pending[0])

        second = self.import_response(source, pending[1])

        self.assertNotEqual(first.visit["visit_id"], second.visit["visit_id"])
        self.assertEqual(len(list((self.root / "visits").glob("*.yaml"))), 2)

    def test_corrected_heading_reordered_unicode_multiline_and_blanks(self):
        headings = (
            PLACE_COLUMN,
            TIMESTAMP_COLUMN,
            VISITORS_COLUMN,
            LOCATION_COLUMN,
            EXPERIENCE_COLUMN,
            VISIT_DATE_COLUMN,
            ADVICE_COLUMN,
            PARKING_COLUMN,
            TOILETS_COLUMN,
            ACCESSIBILITY_COLUMN,
            RECOMMEND_COLUMN,
            AUDIO_COLUMN,
            MEDIA_COLUMN,
        )
        source = FakeGoogleSource(
            [
                fictional_row(
                    1,
                    headings=headings,
                    **{
                        EXPERIENCE_COLUMN: "Fictional café memory,\nwith Unicode ✓.",
                        ADVICE_COLUMN: "",
                        ACCESSIBILITY_COLUMN: "",
                    },
                )
            ],
            headings=headings,
        )
        response_id = self.discover(source).pending_ids[0]

        result = self.import_response(source, response_id, dry_run=True)

        self.assertEqual(result.visit["state"], "Open")
        self.assertEqual(len(result.visit["evidence"]), 1)

    def test_multiple_media_references_create_distinct_evidence(self):
        source = FakeGoogleSource(
            [
                fictional_row(
                    1,
                    **{
                        MEDIA_COLUMN: (
                            "https://drive.example.invalid/photo-one, "
                            "https://drive.example.invalid/video-two"
                        ),
                        AUDIO_COLUMN: "https://drive.example.invalid/audio-one",
                    },
                )
            ]
        )
        response_id = self.discover(source).pending_ids[0]

        result = self.import_response(
            source,
            response_id,
            media_types=("photo", "video"),
            dry_run=True,
        )

        self.assertEqual(
            [item["evidence_type"] for item in result.visit["evidence"]],
            ["note", "photo", "video", "audio"],
        )

    def test_network_failure_leaves_no_private_state_or_visit(self):
        with self.assertRaisesRegex(AtlasImportError, "network failure"):
            self.discover(FailingGoogleSource())

        self.assertFalse(self.state_store.path.exists())
        self.assertFalse((self.root / "visits").exists())

    def test_unknown_heading_remains_pending_until_selected(self):
        headings = HEADINGS + ("Unknown fictional private field",)
        source = FakeGoogleSource(
            [fictional_row(1) + ("Fictional unknown value",)],
            headings=headings,
        )

        response_id = self.discover(source).pending_ids[0]

        with self.assertRaises(AtlasImportError):
            self.import_response(source, response_id, dry_run=True)

        self.assertEqual(self.discover(source).pending_count, 1)
        self.assertFalse((self.root / "visits").exists())

    def test_changed_source_row_is_rejected_without_new_visit(self):
        source = FakeGoogleSource([fictional_row(1)])
        self.discover(source)
        source.batch = SheetResponseBatch(
            headings=HEADINGS,
            rows=(
                fictional_row(
                    1,
                    **{EXPERIENCE_COLUMN: "Changed fictional memory."},
                ),
            ),
        )

        with self.assertRaisesRegex(AtlasImportError, "changed"):
            self.discover(source)

        self.assertFalse((self.root / "visits").exists())

    def test_visit_failure_leaves_response_pending_and_no_mapping(self):
        source = FakeGoogleSource([fictional_row(1)])
        response_id = self.discover(source).pending_ids[0]

        with self.assertRaises(OSError):
            self.import_response(
                source,
                response_id,
                visit_store=FailingVisitStore(),
            )

        self.assertEqual(self.discover(source).pending_count, 1)
        self.assertEqual(list((self.root / "mappings").glob("*.yaml")), [])

    def test_unknown_opaque_response_id_is_rejected(self):
        source = FakeGoogleSource([fictional_row(1)])
        self.discover(source)

        with self.assertRaisesRegex(AtlasImportError, "not found"):
            self.import_response(source, "RSP-FICTIONAL-UNKNOWN")


if __name__ == "__main__":
    unittest.main()
