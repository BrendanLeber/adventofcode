# -*- coding: utf-8 -*-

import unittest
from aoclib.geometry import Rectangle, Point, Size


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

        self.assertRaises(TypeError, lambda: x + (1, 1))

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

        self.assertRaises(TypeError, lambda: x - 13)

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


if __name__ == "__main__":
    unittest.main()
