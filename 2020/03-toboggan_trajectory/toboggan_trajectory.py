# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import pdb
import traceback
from dataclasses import dataclass
from math import prod
from typing import List

SYMBOL_OPEN = "."
SYMBOL_TREE = "#"


@dataclass
class Steps:
    right: int = 0
    down: int = 0


@dataclass
class Size:
    """A height and width in 2-dimensional space."""

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

    def __sub__(self, other: Point) -> Point:
        """Return the difference of two points."""
        return Point(self.x - other.x, self.y - other.y)

    def __add__(self, other: Point) -> Point:
        """Return the sum of two points."""
        return Point(self.x + other.x, self.y + other.y)

    def manhattan_distance(self, other) -> int:
        """Calculate the Manhattan distance between `self` and `other`."""
        return abs(self.x - other.x) + abs(self.y - other.y)


class Field:
    def __init__(self, size: Size, field: List[str]) -> None:
        self.size: Size = size
        self.field: List[str] = field[:]

    def __str__(self) -> str:
        output: str = ""
        for row in range(self.size.cy):
            if len(output) > 0:
                output += "\n"
            offset: int = self.size.cx * row
            extent: int = offset + self.size.cx
            output += "".join(self.field[offset:extent])
        return output

    @property
    def height(self) -> int:
        return self.size.cy

    @property
    def width(self) -> int:
        return self.size.cx

    def at(self, pos: Point) -> str:
        """Return the contents of the field at the given position."""
        if pos.x >= self.size.cx:
            # adjust our horizontal coordinate to account for repeated columns
            pos.x = pos.x % self.size.cx
        if not (0 <= pos.y < self.size.cy):
            raise ValueError(f"pos y value {pos.y} must be between 0 and {self.size.cy}!")
        offset = (self.size.cx * pos.y) + pos.x
        return self.field[offset]


def parse_input(fname: str) -> Field:
    """Read the input file and return the parsed data."""
    data: List[str] = []
    width: int = -1
    height: int = 0
    with open(args.input, "rt") as inf:
        for line in inf:
            line = line.strip()
            if width < 0:
                width = len(line)
            elif width != len(line):
                raise ValueError(f"received {len(line)} characters and expected {width}!")
            height += 1
            data.extend(list(line))
    return Field(Size(width, height), data)


def count_trees(field: Field, steps: Steps) -> int:
    """Count the number trees encountered in the field."""
    trees: int = 0
    pos: Point = Point(0, 0)
    while pos.y < field.height:
        if field.at(pos) == SYMBOL_TREE:
            trees += 1
        pos.offset(steps.right, steps.down)
    return trees


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2020 - Day 3 - Toboggan Trajectory"
    )
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    args = parser.parse_args()

    try:
        field: Field = parse_input(args.input)

        tree_counts: List[int] = [-1] * 5
        steps: List[Steps] = [Steps(1, 1), Steps(3, 1), Steps(5, 1), Steps(7, 1), Steps(1, 2)]
        for idx, step in enumerate(steps):
            tree_counts[idx] = count_trees(field, step)
        one: int = tree_counts[1]
        two: int = prod(tree_counts)
        print((one, two))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
