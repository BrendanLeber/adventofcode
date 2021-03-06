# -*- coding: utf-8 -*-


from dataclasses import dataclass

from point import Point
from size import Size


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
            and self.right >= point.x   # noqa: W503
            and self.top <= point.y     # noqa: W503
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
