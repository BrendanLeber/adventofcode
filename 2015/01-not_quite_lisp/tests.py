# -*- coding: utf-8 -*-


import unittest

from solve import solve


class PartOneTestCases(unittest.TestCase):
    def test_p1_01(self):
        self.assertEqual(solve("(())")[0], 0)
        self.assertEqual(solve("()()")[0], 0)

    def test_p1_02(self):
        self.assertEqual(solve("(((")[0], 3)
        self.assertEqual(solve("(()(()(")[0], 3)

    def test_p1_03(self):
        self.assertEqual(solve("))(((((")[0], 3)

    def test_p1_04(self):
        self.assertEqual(solve("())")[0], -1)
        self.assertEqual(solve("))(")[0], -1)

    def test_p1_05(self):
        self.assertEqual(solve(")))")[0], -3)
        self.assertEqual(solve(")())())")[0], -3)


class PartTwoTestCases(unittest.TestCase):
    def test_p2_01(self):
        self.assertEqual(solve(")")[1], 1)

    def test_p2_02(self):
        self.assertEqual(solve("()())")[1], 5)


if __name__ == "__main__":
    unittest.main()
