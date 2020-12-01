# -*- coding: utf-8 -*-

import unittest
from aoclib.geometry import Point


class PointUnitTests(unittest.TestCase):
    def test_constructor(self):
        default = Point()
        self.assertEqual(default.x, 0)
        self.assertEqual(default.y, 0)

        default = Point(y=25, x=10)
        self.assertEqual(default.x, 10)
        self.assertEqual(default.y, 25)

    def test_offset(self):
        x = Point(100, 100)
        x.offset(35, 35)
        self.assertEqual(x, Point(135, 135))

        x = Point(100, 100)
        x.offset(-25, -50)
        self.assertEqual(x, Point(75, 50))

    def test_operator_eq(self):
        x = Point(256, 128)
        y = Point(256, 128)
        self.assertTrue(x == y)
        self.assertFalse(x is y)

    def test_operator_neq(self):
        x = Point(256, 128)
        y = Point(1024, 4096)
        self.assertTrue(x != y)

    def test_operator_add_eq(self):
        x = Point(100, 100)
        y = Point(35, 35)
        x += y
        self.assertEqual(x, Point(135, 135))
        self.assertEqual(y, Point(35, 35))

    def test_operator_sub_eq(self):
        x = Point(100, 100)
        y = Point(35, 35)
        x -= y
        self.assertEqual(x, Point(65, 65))
        self.assertEqual(y, Point(35, 35))

    def test_operator_add(self):
        x = Point(100, 100)
        y = Point(35, 35)
        z = x + y
        self.assertEqual(z, Point(135, 135))
        self.assertEqual(x, Point(100, 100))
        self.assertEqual(y, Point(35, 35))

    def test_operator_sub(self):
        x = Point(100, 100)
        y = Point(35, 35)
        z = x - y
        self.assertEqual(z, Point(65, 65))
        self.assertEqual(x, Point(100, 100))
        self.assertEqual(y, Point(35, 35))

    def test_manhattan_distance(self):
        x = Point(0, 0)
        self.assertEqual(x.manhattan_distance(Point(0, 0)), 0)
        self.assertEqual(x.manhattan_distance(Point(1, 1)), 2)
        self.assertEqual(x.manhattan_distance(Point(-3, -3)), 6)


if __name__ == "__main__":
    unittest.main()
