# -*- coding: utf-8 -*-

import unittest

from aoclib.geometry import Size


class SizeUnitTests(unittest.TestCase):
    def test_constructor(self):
        sz_default = Size()
        self.assertEqual(sz_default.cx, 0)
        self.assertEqual(sz_default.cy, 0)

        sz_a = Size(10, 25)
        sz_b = Size(cy=25, cx=10)
        self.assertEqual(sz_a, sz_b)

    def test_operator_eq(self):
        sz1 = Size(135, 135)
        sz2 = Size(135, 135)
        self.assertTrue(sz1 == sz2)
        self.assertFalse(sz1 is sz2)

    def test_operator_neq(self):
        sz1 = Size(111, 111)
        sz2 = Size(222, 222)
        self.assertTrue(sz1 != sz2)

    def test_operator_add_eq(self):
        x = Size(100, 100)
        y = Size(50, 25)
        x += y
        self.assertEqual(x, Size(150, 125))
        self.assertEqual(y, Size(50, 25))

    def test_operator_sub_eq(self):
        x = Size(100, 100)
        y = Size(50, 25)
        x -= y
        self.assertEqual(x, Size(50, 75))
        self.assertEqual(y, Size(50, 25))

    def test_operator_add(self):
        x = Size(100, 100)
        y = Size(50, 25)
        z = x + y
        self.assertEqual(x, Size(100, 100))
        self.assertEqual(y, Size(50, 25))
        self.assertEqual(z, Size(150, 125))

    def test_operator_sub(self):
        x = Size(100, 100)
        y = Size(50, 25)
        z = x - y
        self.assertEqual(x, Size(100, 100))
        self.assertEqual(y, Size(50, 25))
        self.assertEqual(z, Size(50, 75))


if __name__ == "__main__":
    unittest.main()
