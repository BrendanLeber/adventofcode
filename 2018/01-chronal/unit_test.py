#!/usr/bin/env python


import unittest
from chronal import part_one


class PartOneTestCases(unittest.TestCase):
    def test_1(self):
        self.assertEqual(part_one([1, -2, 3, 1]), 3)

    def test_2(self):
        """[+1, +1, +1] results in 3."""
        self.assertEqual(part_one([1, 1, 1]), 3)

    def test_3(self):
        """[1, 1, -2] results in 0."""
        self.assertEqual(part_one([1, 1, -2]), 0)

    def test_4(self):
        """[-1, -2, -3] results in -6."""
        self.assertEqual(part_one([-1, -2, -3]), -6)


if __name__ == "__main__":
    unittest.main()
