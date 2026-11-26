import unittest

from summary import count_active_entries, total_active_minutes


class SummaryTests(unittest.TestCase):
    def test_active_records_allow_case_whitespace_and_signed_minutes(self) -> None:
        records = [" ACTIVE : 7", "inactive: ignored", "active: -2"]
        self.assertEqual(5, total_active_minutes(records))
        self.assertEqual(2, count_active_entries(records))

    def test_empty_records(self) -> None:
        self.assertEqual(0, total_active_minutes([]))
        self.assertEqual(0, count_active_entries([]))

    def test_only_total_converts_active_minutes(self) -> None:
        self.assertEqual(1, count_active_entries(["active: invalid"]))
        with self.assertRaises(ValueError):
            total_active_minutes(["active: invalid"])

    def test_both_operations_reject_a_missing_separator(self) -> None:
        for summarize in (total_active_minutes, count_active_entries):
            with self.subTest(summarize=summarize.__name__), self.assertRaises(ValueError):
                summarize(["inactive"])
