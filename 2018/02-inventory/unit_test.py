#!/usr/bin/env python


import unittest
from inventory import part_one, part_two


class PartOneTestCases(unittest.TestCase):
    def test_1_1(self):
        package_ids = ["abcdef", "bababc", "abbcde", "abcccd", "aabcdd", "abcdee", "ababab"]
        self.assertEqual(part_one(package_ids), 12)


class PartTwoTestCases(unittest.TestCase):
    def test_2_1(self):
        package_ids = ["abcde", "fghij", "klmno", "pqrst", "fguij", "axcye"]
        self.assertEqual(part_two(package_ids), "fgij")


if __name__ == "__main__":
    unittest.main()
