import unittest
from solution import median

class TestMedian(unittest.TestCase):
    def test_odd(self):
        self.assertEqual(median([3, 1, 2]), 2)

    def test_even(self):
        self.assertEqual(median([1, 3, 5, 7]), 4)
