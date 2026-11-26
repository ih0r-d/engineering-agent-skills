import unittest

from after import first_matches


class FirstMatchesTests(unittest.TestCase):
    def test_limits_matching_items_at_the_start(self) -> None:
        self.assertEqual(["amber", "azure"], first_matches(["amber", "azure", "bronze"], "a", 2))

    def test_zero_limit(self) -> None:
        self.assertEqual([], first_matches(["amber"], "a", 0))
