#!/usr/bin/env python

"""
Solve the Advent of Code Day 06 problem:
'Probably a Fire Hazard'.
"""

from collections import namedtuple
from dataclasses import dataclass
import fileinput
import re
import sys


@dataclass
class Size:
    """A height and width in 2-dimensional space."""

    cx: int = 0
    cy: int = 0

    def __add__(self, rhs):
        """Return the sum of two sizes."""
        return Size(self.cx + rhs.cx, self.cy + rhs.cy)

    def __sub__(self, rhs):
        """Return the difference of two sizes."""
        return Size(self.cx - rhs.cx, self.cy - rhs.cy)


@dataclass
class Point:
    """A point in 2-dimensional space."""

    x: int = 0
    y: int = 0

    def offset(self, x_offset, y_offset):
        """Offset the point by the given values."""
        self.x += x_offset
        self.y += y_offset

    def __sub__(self, rhs):
        """Return the difference of two points."""
        return Point(self.x - rhs.x, self.y - rhs.y)

    def __add__(self, rhs):
        """Return the sum of two points."""
        return Point(self.x + rhs.x, self.y + rhs.y)


@dataclass
class Rect:
    """A rectangle in 2-dimensional space."""

    left: int = 0
    top: int = 0
    right: int = 0
    bottom: int = 0

    def bottom_right(self):
        """Return the bottom-right point of the rectangle."""
        return Point(self.right, self.bottom)

    def center_point(self):
        """Return the center point of the rectangle."""
        return Point(self.left + (self.width() // 2), self.top + (self.height() // 2))

    def width(self):
        """Return the width of the rectangle."""
        return self.right - self.left

    def height(self):
        """Return the height of the rectangle."""
        return self.bottom - self.top

    def deflate(self, cx, cy):
        """Deflate the rectangle by moving the sides towards the center."""
        self.left += cx
        self.top += cy
        self.right -= cx
        self.bottom -= cy

    def deflate_rect(self, rhs):
        """Deflate the rectangle by moving the sides towards the center."""
        self.left += rhs.left
        self.top += rhs.top
        self.right -= rhs.right
        self.bottom -= rhs.bottom

    def inflate(self, cx, cy):
        """Inflate the rectangle by moving the sides away from the center."""
        self.left -= cx
        self.top -= cy
        self.right += cx
        self.bottom += cy

    def inflate_rect(self, rhs):
        """Inflate the rectangle by moving the sides away from the center."""
        self.left -= rhs.left
        self.top -= rhs.top
        self.right += rhs.right
        self.bottom += rhs.bottom

    @staticmethod
    def intersect(lhs, rhs):
        """Create a rectangle equal to the intersection of the given rectangles."""
        return Rect(
            max(lhs.left, rhs.left),
            max(lhs.top, rhs.top),
            min(lhs.right, rhs.right),
            min(lhs.bottom, rhs.bottom),
        )

    def is_empty(self):
        """Return True if the rectangle height and or width are <= 0."""
        return self.height() <= 0 or self.width() <= 0

    def is_null(self):
        """Return True if all values in the rectangle are 0."""
        return self.left == 0 and self.top == 0 and self.right == 0 and self.bottom == 0

    def move_to_x(self, x):
        """Move the rectangle to the absolute coordinate specified by x."""
        self.right = self.width() + x
        self.left = x

    def move_to_y(self, y):
        """Move the rectangle to the absolute coordinate specified by y."""
        self.bottom = self.height() + y
        self.top = y

    def move_to_xy(self, x, y):
        """Move the rectangle to the absolute x- and y- coordinates specified."""
        self.move_to_x(x)
        self.move_to_y(y)

    def normalize(self):
        """Normalizes the rectangle so both the height and the width are positive."""
        if self.left > self.right:
            self.left, self.right = self.right, self.left
        if self.top > self.bottom:
            self.top, self.bottom = self.bottom, self.top

    def offset(self, x_offset, y_offset):
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
        elif isinstance(rhs, Rect):
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
        elif isinstance(rhs, Rect):
            new_rect.left -= rhs.left
            new_rect.top -= rhs.top
            new_rect.right -= rhs.right
            new_rect.bottom -= rhs.bottom
        else:
            raise TypeError("rhs must be a Point or a Rect.")
        return new_rect

    def pt_in_rect(self, point):
        """Returns True if the given point is inside the rectangle."""
        return (
            self.left <= point.x
            and self.right >= point.x
            and self.top <= point.y
            and self.bottom >= point.y
        )

    def set(self, left, top, right, bottom):
        """Set the dimension of the rectangle."""
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

    def set_empty(self):
        """Make a null rectangle by setting all coordinates to zero."""
        self.left = 0
        self.top = 0
        self.right = 0
        self.bottom = 0

    def size(self):
        """Get a Size object representing the width and height of the rectangle."""
        return Size(self.width(), self.height())

    # @staticmethod
    # def subtract_rect(lhs, rhs):
    #     '''Create a rectangle with dimensions equal to the subtraction of lhs from rhs.'''
    #     return Rect()

    @staticmethod
    def union(lhs, rhs):
        """Make a rectangle that is a union of the two given rectangles."""
        return Rect(
            min(lhs.left, rhs.left),
            min(lhs.top, rhs.top),
            max(lhs.right, rhs.right),
            max(lhs.bottom, rhs.bottom),
        )


Order = namedtuple("Order", ["cmd", "rect"])


def turn_on_lights(lights, rect):
    """Turn on lights in the given rectangle."""
    for row in range(rect.top, rect.bottom + 1):
        for col in range(rect.left, rect.right + 1):
            lights[row][col] = 1


def turn_off_lights(lights, rect):
    """Turn off lights in the given rectangle."""
    for row in range(rect.top, rect.bottom + 1):
        for col in range(rect.left, rect.right + 1):
            lights[row][col] = 0


def toggle_lights(lights, rect):
    """Turn on lights in the given rectangle."""
    for row in range(rect.top, rect.bottom + 1):
        for col in range(rect.left, rect.right + 1):
            if lights[row][col] == 1:
                lights[row][col] = 0
            else:
                lights[row][col] = 1


def solve_part_1(orders):
    """Solve the first part of the puzzle."""

    lights = [[0] * 1000 for i in range(1000)]
    # for row in lights:
    #     print(' '.join([str(elem) for elem in row]))

    for order in orders:
        if order.cmd == "turn on":
            turn_on_lights(lights, order.rect)
        elif order.cmd == "turn off":
            turn_off_lights(lights, order.rect)
        elif order.cmd == "toggle":
            toggle_lights(lights, order.rect)
        else:
            raise TypeError(f"unknown command ({order.cmd})")

    lights_lit = 0
    for row in range(1000):
        for col in range(1000):
            lights_lit += lights[row][col]

    return lights_lit


def solve_part_2(orders):
    """Solve the second part of the puzzle."""
    lights = [[0] * 1000 for i in range(1000)]

    for order in orders:
        if order.cmd == "turn on":
            for row in range(order.rect.top, order.rect.bottom + 1):
                for col in range(order.rect.left, order.rect.right + 1):
                    lights[row][col] += 1
        elif order.cmd == "turn off":
            for row in range(order.rect.top, order.rect.bottom + 1):
                for col in range(order.rect.left, order.rect.right + 1):
                    if lights[row][col] > 0:
                        lights[row][col] -= 1
        elif order.cmd == "toggle":
            for row in range(order.rect.top, order.rect.bottom + 1):
                for col in range(order.rect.left, order.rect.right + 1):
                    lights[row][col] += 2
        else:
            raise TypeError(f"unknown command ({order.cmd})")

    brightness = 0
    for row in range(1000):
        for col in range(1000):
            brightness += lights[row][col]

    return brightness


def solve(orders):
    """Solve the puzzle."""
    return (solve_part_1(orders), solve_part_2(orders))


if __name__ == "__main__":
    # read problem input from file or stdin
    pattern = re.compile(
        r"^(?P<cmd>turn on|turn off|toggle|) +(?P<left>[0-9]+),(?P<top>[0-9]+) +through +(?P<right>[0-9]+),(?P<bottom>[0-9]+)$"
    )
    data = []
    for line in fileinput.input():
        matches = pattern.search(line.strip())
        if not matches:
            raise TypeError("input line does not match expected format.")

        rc = Rect(
            int(matches.group("left")),
            int(matches.group("top")),
            int(matches.group("right")),
            int(matches.group("bottom")),
        )
        data.append(Order(cmd=matches.group("cmd"), rect=rc))

    print(solve(data))
