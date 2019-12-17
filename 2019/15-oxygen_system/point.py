# -*- coding: utf-8 -*-


from dataclasses import dataclass


@dataclass
class Point:
    """A point in 2-dimensional space."""

    x: int = 0
    y: int = 0

    def offset(self, x_offset: int, y_offset: int):
        """Offset the point by the given values."""
        self.x += x_offset
        self.y += y_offset

    def __sub__(self, rhs):
        """Return the difference of two points."""
        return Point(self.x - rhs.x, self.y - rhs.y)

    def __add__(self, rhs):
        """Return the sum of two points."""
        return Point(self.x + rhs.x, self.y + rhs.y)


if __name__ == "__main__":
    import unittest

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

    unittest.main()
