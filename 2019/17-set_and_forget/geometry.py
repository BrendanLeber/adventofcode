# -*- coding: utf-8 -*-

from __future__ import annotations

from dataclasses import dataclass
from typing import Tuple


@dataclass
class Size:
    """A height and width in 2-dimensional space.

    Attributes
    ----------
    cx : int
        The width component of the Size.
    cy : int
        The height component of the Size.

    Methods
    -------
    __add__
    """

    cx: int = 0
    cy: int = 0

    def __add__(self, other: Size) -> Size:
        """Return the sum of two sizes."""
        return Size(self.cx + other.cx, self.cy + other.cy)

    def __sub__(self, other: Size) -> Size:
        """Return the difference of two sizes."""
        return Size(self.cx - other.cx, self.cy - other.cy)


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

    def manhattan_distance(self, other) -> int:
        """Calculate the Manhattan distance between `self` and `other`."""
        return abs(self.x - other.x) + abs(self.y - other.y)


@dataclass
class Rectangle:
    """A rectangle in 2-dimensional space."""

    left: int = 0
    top: int = 0
    right: int = 0
    bottom: int = 0

    def bottom_right(self) -> Point:
        """Return the bottom-right point of the rectangle."""
        return Point(self.right, self.bottom)

    def center_point(self) -> Point:
        """Return the center point of the rectangle."""
        return Point(self.left + (self.width() // 2), self.top + (self.height() // 2))

    def width(self) -> int:
        """Return the width of the rectangle."""
        return self.right - self.left

    def height(self) -> int:
        """Return the height of the rectangle."""
        return self.bottom - self.top

    def deflate(self, cx: int, cy: int) -> None:
        """Deflate the rectangle by moving the sides towards the center."""
        self.left += cx
        self.top += cy
        self.right -= cx
        self.bottom -= cy

    def deflate_rect(self, rhs) -> None:
        """Deflate the rectangle by moving the sides towards the center."""
        self.left += rhs.left
        self.top += rhs.top
        self.right -= rhs.right
        self.bottom -= rhs.bottom

    def inflate(self, cx: int, cy: int) -> None:
        """Inflate the rectangle by moving the sides away from the center."""
        self.left -= cx
        self.top -= cy
        self.right += cx
        self.bottom += cy

    def inflate_rect(self, rhs) -> None:
        """Inflate the rectangle by moving the sides away from the center."""
        self.left -= rhs.left
        self.top -= rhs.top
        self.right += rhs.right
        self.bottom += rhs.bottom

    def intersect(self, other):
        """Create a rectangle equal to the intersection of the given rectangles."""
        return Rectangle(
            max(self.left, other.left),
            max(self.top, other.top),
            min(self.right, other.right),
            min(self.bottom, other.bottom),
        )

    def is_empty(self) -> bool:
        """Return True if the rectangle height and or width are <= 0."""
        return self.height() <= 0 or self.width() <= 0

    def is_null(self) -> bool:
        """Return True if all values in the rectangle are 0."""
        return self.left == 0 and self.top == 0 and self.right == 0 and self.bottom == 0

    def move_to_x(self, x: int) -> None:
        """Move the rectangle to the absolute coordinate specified by x."""
        self.right = self.width() + x
        self.left = x

    def move_to_y(self, y: int) -> None:
        """Move the rectangle to the absolute coordinate specified by y."""
        self.bottom = self.height() + y
        self.top = y

    def move_to_xy(self, x: int, y: int) -> None:
        """Move the rectangle to the absolute x- and y- coordinates specified."""
        self.move_to_x(x)
        self.move_to_y(y)

    def normalize(self) -> None:
        """Normalizes the rectangle so both the height and the width are positive."""
        if self.left > self.right:
            self.left, self.right = self.right, self.left
        if self.top > self.bottom:
            self.top, self.bottom = self.bottom, self.top

    def offset(self, x_offset: int, y_offset: int) -> None:
        """Offset the point by the given values."""
        self.left += x_offset
        self.top += y_offset
        self.right += x_offset
        self.bottom += y_offset

    def __add__(self, rhs):
        """Displace the rectangle by the specified offsets."""
        new_rect = self
        if isinstance(rhs, Point):
            new_rect.left += rhs.x
            new_rect.top += rhs.y
            new_rect.right += rhs.x
            new_rect.bottom += rhs.y
        elif isinstance(rhs, Rectangle):
            new_rect.left += rhs.left
            new_rect.top += rhs.top
            new_rect.right += rhs.right
            new_rect.bottom += rhs.bottom
        else:
            raise TypeError("rhs must be a Point or a Rect.")
        return new_rect

    def __sub__(self, rhs):
        """Displace the rectangle by the specified offsets."""
        new_rect = self
        if isinstance(rhs, Point):
            new_rect.left -= rhs.x
            new_rect.top -= rhs.y
            new_rect.right -= rhs.x
            new_rect.bottom -= rhs.y
        elif isinstance(rhs, Rectangle):
            new_rect.left -= rhs.left
            new_rect.top -= rhs.top
            new_rect.right -= rhs.right
            new_rect.bottom -= rhs.bottom
        else:
            raise TypeError("rhs must be a Point or a Rect.")
        return new_rect

    def pt_in_rect(self, point: Point) -> bool:
        """Returns True if the given point is inside the rectangle."""
        return (
            self.left <= point.x
            and self.right >= point.x  # noqa: W503
            and self.top <= point.y  # noqa: W503
            and self.bottom >= point.y  # noqa: W503
        )

    def set(self, left: int, top: int, right: int, bottom: int) -> None:
        """Set the dimension of the rectangle."""
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def set_empty(self) -> None:
        """Make a null rectangle by setting all coordinates to zero."""
        self.left = 0
        self.top = 0
        self.right = 0
        self.bottom = 0

    def size(self) -> Size:
        """Get a Size object representing the width and height of the rectangle."""
        return Size(self.width(), self.height())

    # def subtract_rect(lhs, rhs):
    #     """Create a rectangle with dimensions equal to the subtraction of lhs from rhs."""
    #     return Rectangle()

    def top_left(self) -> Point:
        """Return the top-left point of the rectangle."""
        return Point(self.left, self.top)

    def union(self, other):
        """Make a rectangle that is a union of the two given rectangles."""
        return Rectangle(
            min(self.left, other.left),
            min(self.top, other.top),
            max(self.right, other.right),
            max(self.bottom, other.bottom),
        )


def manhattan_distance(a: Tuple[int, int], b: Tuple[int, int]) -> int:
    """Return the Manhattan distance between two points."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


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

    class RectangleUnitTests(unittest.TestCase):
        def test_constructor(self):
            rc = Rectangle()
            self.assertEqual(rc.left, 0)
            self.assertEqual(rc.top, 0)
            self.assertEqual(rc.right, 0)
            self.assertEqual(rc.bottom, 0)

            rc = Rectangle(top=10, bottom=100, right=128, left=16)
            self.assertEqual(rc.left, 16)
            self.assertEqual(rc.top, 10)
            self.assertEqual(rc.right, 128)
            self.assertEqual(rc.bottom, 100)

        def test_operator_assign(self):
            x = Rectangle(0, 0, 127, 128)
            y = x
            self.assertEqual(y, Rectangle(0, 0, 127, 128))

        def test_operator_eq(self):
            x = Rectangle(35, 150, 10, 25)
            y = Rectangle(35, 150, 10, 25)
            z = Rectangle(98, 999, 6, 3)
            self.assertTrue(x == y)
            self.assertFalse(x is y)
            self.assertFalse(x == z)

        def test_operator_not_eq(self):
            x = Rectangle(35, 150, 10, 25)
            y = Rectangle(35, 150, 10, 25)
            z = Rectangle(98, 999, 6, 3)
            self.assertFalse(x != y)
            self.assertFalse(x is y)
            self.assertTrue(x != z)

        def test_operator_add(self):
            x = Rectangle(100, 235, 200, 335)
            y = x + Point(35, 65)
            self.assertEqual(y, Rectangle(135, 300, 235, 400))
            x = Rectangle(100, 235, 200, 335)
            y = x + Rectangle(1, 2, 3, 4)
            self.assertEqual(y, Rectangle(101, 237, 203, 339))

        def test_operator_add_eq(self):
            x = Rectangle(100, 235, 200, 335)
            x += Point(35, 65)
            self.assertEqual(x, Rectangle(135, 300, 235, 400))
            x = Rectangle(100, 235, 200, 335)
            x += Rectangle(1, 2, 3, 4)
            self.assertEqual(x, Rectangle(101, 237, 203, 339))

        def test_operator_sub(self):
            x = Rectangle(100, 235, 200, 335)
            y = x - Point(35, 65)
            self.assertEqual(y, Rectangle(65, 170, 165, 270))
            x = Rectangle(100, 235, 200, 335)
            y = x - Rectangle(1, 2, 3, 4)
            self.assertEqual(y, Rectangle(99, 233, 197, 331))

        def test_operator_sub_eq(self):
            x = Rectangle(100, 235, 200, 335)
            x -= Point(35, 65)
            self.assertEqual(x, Rectangle(65, 170, 165, 270))
            x = Rectangle(100, 235, 200, 335)
            x -= Rectangle(1, 2, 3, 4)
            self.assertEqual(x, Rectangle(99, 233, 197, 331))

        def test_bottom_right(self):
            rc = Rectangle(210, 150, 350, 900)
            pt = rc.bottom_right()
            self.assertTrue(isinstance(pt, Point))
            self.assertEqual(pt, Point(350, 900))

        def test_center_point(self):
            rc = Rectangle(210, 150, 350, 900)
            pt = rc.center_point()
            self.assertTrue(isinstance(pt, Point))
            self.assertEqual(pt, Point(280, 525))

        def test_deflates(self):
            rc = Rectangle(10, 10, 50, 50)
            rc.deflate(1, 2)
            self.assertEqual(rc, Rectangle(11, 12, 49, 48))

            rc = Rectangle(10, 10, 50, 50)
            rc.deflate_rect(Rectangle(1, 2, 3, 4))
            self.assertEqual(rc, Rectangle(11, 12, 47, 46))

        def test_height_and_width(self):
            rc = Rectangle(20, 30, 80, 70)
            self.assertEqual(rc.height(), 40)
            self.assertEqual(rc.width(), 60)

        def test_inflates(self):
            rc = Rectangle(0, 0, 300, 300)
            rc.inflate(50, 200)
            self.assertEqual(rc, Rectangle(-50, -200, 350, 500))

            rc = Rectangle(0, 0, 300, 300)
            rc.inflate_rect(Rectangle(50, 60, 300, 310))
            self.assertEqual(rc, Rectangle(-50, -60, 600, 610))

        def test_intersect(self):
            rc = Rectangle(125, 0, 150, 200)
            result = rc.intersect(Rectangle(0, 75, 350, 95))
            self.assertEqual(result, Rectangle(125, 75, 150, 95))

        def test_is_empty(self):
            none = Rectangle()
            some = Rectangle(35, 50, 135, 150)
            null = Rectangle(35, 35, 35, 35)
            self.assertTrue(none.is_empty())
            self.assertFalse(some.is_empty())
            self.assertTrue(null.is_empty())

        def test_is_null(self):
            none = Rectangle()
            some = Rectangle(35, 50, 135, 150)
            null = Rectangle(35, 35, 35, 35)
            self.assertTrue(none.is_null())
            self.assertFalse(some.is_null())
            self.assertFalse(null.is_null())

        def test_move_to_x(self):
            rc = Rectangle(0, 0, 100, 100)
            rc.move_to_x(10)
            self.assertEqual(rc, Rectangle(10, 0, 110, 100))

        def test_move_to_xy(self):
            rc = Rectangle(0, 0, 100, 100)
            rc.move_to_xy(10, 20)
            self.assertEqual(rc, Rectangle(10, 20, 110, 120))

        def test_move_to_y(self):
            rc = Rectangle(0, 0, 100, 100)
            rc.move_to_y(20)
            self.assertEqual(rc, Rectangle(0, 20, 100, 120))

        def test_normalize(self):
            x = Rectangle(110, 100, 250, 310)
            x.normalize()
            y = Rectangle(250, 310, 110, 100)
            y.normalize()
            self.assertEqual(x, y)

            x = Rectangle(0, 0, 100, 100)
            x.normalize()
            self.assertEqual(x, Rectangle(0, 0, 100, 100))

        def test_offset(self):
            x = Rectangle(0, 0, 35, 35)
            x.offset(230, 230)
            self.assertEqual(x, Rectangle(230, 230, 265, 265))

        def test_pt_in_rect(self):
            x = Rectangle(5, 5, 100, 100)
            self.assertTrue(x.pt_in_rect(Point(35, 50)))
            self.assertFalse(x.pt_in_rect(Point(125, 298)))

        def test_sets(self):
            x = Rectangle()
            self.assertEqual(x, Rectangle(0, 0, 0, 0))
            x.set(256, 256, 512, 512)
            self.assertEqual(x, Rectangle(256, 256, 512, 512))
            x.set_empty()
            self.assertEqual(x, Rectangle())

        def test_size(self):
            x = Rectangle(10, 10, 50, 50)
            sz = x.size()
            self.assertTrue(isinstance(sz, Size))
            self.assertEqual(sz, Size(40, 40))

        # def test_subtract_rect(self):
        #     x = Rectangle(10, 10, 100, 100)
        #     y = Rectangle(50, 10, 150, 150)
        #     z = x.subtract_rect(y)
        #     self.assertEqual(x, Rectangle(10, 10, 50, 100))

        def test_top_left(self):
            x = Rectangle(128, 128, 256, 256)
            pt = x.top_left()
            self.assertTrue(isinstance(pt, Point))
            self.assertEqual(pt, Point(128, 128))

        def test_union(self):
            x = Rectangle(100, 0, 200, 300)
            y = Rectangle(0, 100, 300, 200)
            z = x.union(y)
            self.assertEqual(z, Rectangle(0, 0, 300, 300))

        def test_width(self):
            x = Rectangle(20, 30, 80, 70)
            self.assertEqual(x.width(), 60)

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

    unittest.main()
