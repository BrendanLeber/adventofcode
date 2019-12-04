# -*- coding: utf-8 -*-


import unittest

from solve import valid_password1, valid_password2


class ValidPasswordOneTestCases(unittest.TestCase):
    def test_vp1_01(self):
        self.assertTrue(valid_password1("111111"))

    def test_vp1_02(self):
        self.assertFalse(valid_password1("223450"))

    def test_vp1_03(self):
        self.assertFalse(valid_password1("123789"))


class ValidPasswordTwoTestCases(unittest.TestCase):
    def test_vp2_01(self):
        self.assertTrue(valid_password2("112233"))

    def test_vp2_02(self):
        self.assertFalse(valid_password2("123444"))

    def test_vp2_03(self):
        self.assertTrue(valid_password2("111122"))


if __name__ == "__main__":
    unittest.main()
