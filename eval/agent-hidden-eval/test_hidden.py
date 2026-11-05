import unittest
from solution import median

class HiddenTests(unittest.TestCase):
    def test_negative_even(self):
        self.assertEqual(median([-7, -1, 3, 5]), 1)

    def test_duplicates(self):
        self.assertEqual(median([9, 1, 1, 1]), 1)

    def test_float(self):
        self.assertEqual(median([0.1, 0.3]), 0.2)

    def test_single(self):
        self.assertEqual(median([42]), 42)

    def test_even_unsorted(self):
        self.assertEqual(median([8, 1, 2, 7]), 4.5)

    def test_empty(self):
        with self.assertRaises(ValueError):
            median([])
