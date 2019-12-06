# -*- coding: utf-8 -*-


import unittest

from solve import solve


class PartOneTestCases(unittest.TestCase):
    def test_p1_01(self):
        self.assertEqual(solve([(2, 3, 4)])[0], 58)

    def test_p1_02(self):
        self.assertEqual(solve([(1, 1, 10)])[0], 43)


class PartTwoTestCases(unittest.TestCase):
    def test_p2_01(self):
        self.assertEqual(solve([(2, 3, 4)])[1], 34)

    def test_p2_02(self):
        self.assertEqual(solve([(1, 1, 10)])[1], 14)


if __name__ == "__main__":
    unittest.main()
