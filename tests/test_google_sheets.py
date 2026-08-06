"""Tests for the read-only Google Sheets connection checkpoint."""

from pathlib import Path
import tempfile
import unittest

import yaml

from visit_capture.google_sheets import (
    GoogleSheetsCheckError,
    READ_ONLY_SCOPE,
    ensure_private_path,
    inspect_structure,
    load_private_connection,
)


class FakeRequest:
    def __init__(self, result):
        self.result = result

    def execute(self):
        return self.result


class FakeValues:
    def batchGet(self, **arguments):
        self.arguments = arguments
        return FakeRequest(
            {
                "valueRanges": [
                    {
                        "values": [
                            [
                                "Timestamp",
                                "What place did you visit?",
                                "Where is it?",
                                "Who went on the vist? (private)",
                            ]
                        ]
                    },
                    {"values": [["fictional-timestamp"], ["fictional-timestamp"]]},
                ]
            }
        )


class FakeSpreadsheets:
    def __init__(self):
        self._values = FakeValues()

    def get(self, **arguments):
        self.metadata_arguments = arguments
        return FakeRequest(
            {"sheets": [{"properties": {"title": "Fictional responses"}}]}
        )

    def values(self):
        return self._values


class FakeService:
    def __init__(self):
        self.sheets = FakeSpreadsheets()

    def spreadsheets(self):
        return self.sheets


class GoogleSheetsCheckpointTests(unittest.TestCase):
    def test_scope_is_strictly_read_only(self):
        self.assertEqual(
            READ_ONLY_SCOPE,
            "https://www.googleapis.com/auth/spreadsheets.readonly",
        )

    def test_repository_paths_are_rejected(self):
        with self.assertRaises(GoogleSheetsCheckError):
            ensure_private_path(
                Path(__file__).parent / "credentials.json",
                "OAuth client file",
            )

    def test_private_connection_loads_outside_repository(self):
        with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as root:
            connection = Path(root) / "sheet-connection.yaml"
            connection.write_text(
                yaml.safe_dump(
                    {
                        "spreadsheet_id": "fictional-sheet-id",
                        "worksheet_title": "Fictional responses",
                    }
                ),
                encoding="utf-8",
            )
            self.assertEqual(
                load_private_connection(connection),
                ("fictional-sheet-id", "Fictional responses"),
            )

    def test_structure_check_returns_counts_without_response_values(self):
        service = FakeService()

        result = inspect_structure(
            service, "fictional-sheet-id", "Fictional responses"
        )

        self.assertTrue(result.worksheet_accessible)
        self.assertEqual(result.heading_count, 4)
        self.assertEqual(result.recognised_heading_count, 4)
        self.assertEqual(result.response_row_count, 2)
        self.assertEqual(
            service.sheets._values.arguments["ranges"],
            ["'Fictional responses'!1:1", "'Fictional responses'!A2:A"],
        )


if __name__ == "__main__":
    unittest.main()
