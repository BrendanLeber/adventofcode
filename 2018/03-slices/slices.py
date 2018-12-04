#!/usr/bin/env python


from collections import namedtuple
from dataclasses import dataclass
import fileinput
import re


Claim = namedtuple("Claim", ["claim", "area"])


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


def part_one(claims: list) -> int:
    fabric = [[0] * 1000 for _ in range(1000)]

    for claim in claims:
        for row in range(claim.area.top, claim.area.bottom):
            for col in range(claim.area.left, claim.area.right):
                fabric[row][col] += 1

    overlaps = 0
    for row in fabric:
        for col in row:
            if col > 1:
                overlaps += 1

    return overlaps


if __name__ == "__main__":
    pattern = re.compile(
        r"""
        ^\#(?P<claim>[0-9]+) \s+@\s+
        (?P<from_left>[0-9]+) , (?P<from_top>[0-9]+)
        :\s+
        (?P<width>[0-9]+) x (?P<height>[0-9]+)$""",
        re.VERBOSE,
    )

    claims = []
    for line in fileinput.input():
        matches = pattern.search(line.strip())
        if not matches:
            raise TypeError(f"input line does not match expected format: '{line}'")
        area = Rect(
            int(matches.group("from_left")),
            int(matches.group("from_top")),
            int(matches.group("from_left")) + int(matches.group("width")),
            int(matches.group("from_top")) + int(matches.group("height")),
        )
        claims.append(Claim(int(matches.group("claim")), area))

    print(part_one(claims))
