#!/usr/bin/env python


import unittest
from chronal import part_one, part_two


class PartOneTestCases(unittest.TestCase):
    def test_1_1(self):
        self.assertEqual(part_one([1, -2, 3, 1]), 3)

    def test_1_2(self):
        """[+1, +1, +1] results in 3."""
        self.assertEqual(part_one([1, 1, 1]), 3)

    def test_1_3(self):
        """[1, 1, -2] results in 0."""
        self.assertEqual(part_one([1, 1, -2]), 0)

    def test_1_4(self):
        """[-1, -2, -3] results in -6."""
        self.assertEqual(part_one([-1, -2, -3]), -6)


class PartTwoTestCases(unittest.TestCase):
    def test_2_1(self):
        self.assertEqual(part_two([1, -2, 3, 1]), 2)

    def test_2_2(self):
        """[+1, -1] results in 0."""
        self.assertEqual(part_two([1, -1]), 0)

    def test_2_3(self):
        """[3, 3, 4, -2, -4] results in 10."""
        self.assertEqual(part_two([3, 3, 4, -2, -4]), 10)

    def test_2_4(self):
        """[-6, 3, 8, 5, -6] results in 5."""
        self.assertEqual(part_two([-6, 3, 8, 5, -6]), 5)

    def test_2_5(self):
        """[7, 7, -2, -7, -4] results in 14."""
        self.assertEqual(part_two([7, 7, -2, -7, -4]), 14)


if __name__ == "__main__":
    unittest.main()
