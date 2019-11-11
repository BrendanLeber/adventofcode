# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from copy import deepcopy
from typing import List, Tuple

import numpy as np  # type: ignore


class Board:
    def __init__(self, lines: List[str]) -> None:
        self.height: int = len(lines)
        self.width: int = len(lines[0])
        self.cells = np.zeros((self.height, self.width), dtype=bool)
        for row, line in enumerate(lines):
            for col, cell in enumerate(line):
                self.cells[row, col] = True if cell == "#" else False

    def size(self) -> int:
        return self.height * self.width

    def __repr__(self) -> str:
        return f"Board(height={self.height}, width={self.width}, cells={self.cells!r})"

    def __str__(self) -> str:
        result = ""
        for row in range(self.height):
            for col in range(self.width):
                result += "#" if self.cells[row, col] else "."
            result += "\n"
        return result.strip()

    def step(self) -> None:
        neighbors = np.zeros((self.height, self.width), dtype=int)

        # top row
        neighbors[0, 0] = sum([self.cells[0, 1], self.cells[1, 0], self.cells[1, 1]])
        for col in range(1, self.width - 1):
            neighbors[0, col] = sum(
                [
                    self.cells[0, col - 1],
                    self.cells[0, col + 1],
                    self.cells[1, col - 1],
                    self.cells[1, col],
                    self.cells[1, col + 1],
                ]
            )
        neighbors[0, self.width - 1] = sum(
            [
                self.cells[0, self.width - 2],
                self.cells[1, self.width - 2],
                self.cells[1, self.width - 1],
            ]
        )

        # middle rows
        for row in range(1, self.height - 1):
            neighbors[row, 0] = sum(
                [
                    self.cells[row - 1, 0],
                    self.cells[row + 1, 0],
                    self.cells[row - 1, 1],
                    self.cells[row, 1],
                    self.cells[row + 1, 1],
                ]
            )

            for col in range(1, self.width - 1):
                neighbors[row, col] = sum(
                    [
                        self.cells[row - 1, col - 1],
                        self.cells[row - 1, col],
                        self.cells[row - 1, col + 1],
                        self.cells[row, col - 1],
                        self.cells[row, col + 1],
                        self.cells[row + 1, col - 1],
                        self.cells[row + 1, col],
                        self.cells[row + 1, col + 1],
                    ]
                )

            neighbors[row, self.width - 1] = sum(
                [
                    self.cells[row - 1, self.width - 1],
                    self.cells[row + 1, self.width - 1],
                    self.cells[row - 1, self.width - 2],
                    self.cells[row, self.width - 2],
                    self.cells[row + 1, self.width - 2],
                ]
            )

        # bottom row
        neighbors[self.height - 1, 0] = sum(
            [
                self.cells[self.height - 2, 0],
                self.cells[self.height - 2, 1],
                self.cells[self.height - 1, 1],
            ]
        )
        for col in range(1, self.width - 1):
            neighbors[self.height - 1, col] = sum(
                [
                    self.cells[self.height - 2, col - 1],
                    self.cells[self.height - 2, col],
                    self.cells[self.height - 2, col + 1],
                    self.cells[self.height - 1, col - 1],
                    self.cells[self.height - 1, col + 1],
                ]
            )
        neighbors[self.height - 1, self.width - 1] = sum(
            [
                self.cells[self.height - 1, self.width - 2],
                self.cells[self.height - 2, self.width - 2],
                self.cells[self.height - 2, self.width - 1],
            ]
        )

        self.cells = (neighbors == 3) | (self.cells & (neighbors == 2))

    def count(self) -> int:
        """Count the number of lit cells."""
        return sum(sum(self.cells))  # type: ignore

    def light_corners(self) -> None:
        """Force the four corners to always be lit."""
        self.cells[0, 0] = True  # upper, left
        self.cells[0, self.width - 1] = True  # upper, right
        self.cells[self.height - 1, 0] = True  # lower, left
        self.cells[self.height - 1, self.width - 1] = True  # lower, right


def solve(steps: int, board: Board, show: bool) -> Tuple[int, int]:
    one = deepcopy(board)
    if show:
        print(f"Initial state:\n{one}\n")
    for step in range(steps):
        one.step()
        if show:
            print(f"After {step+1} step(s):\n{one}\n")
    if show:
        print(f"Part One:\n{one}\n")

    two = deepcopy(board)
    two.light_corners()
    if show:
        print(f"Initial state:\n{two}\n")
    for step in range(steps):
        two.step()
        two.light_corners()
        if show:
            print(f"After {step+1} step(s):\n{two}\n")
    if show:
        print(f"Part Two:\n{two}\n")

    return (one.count(), two.count())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2015 - Day 18 - Like a GIF For Your Yard."
    )
    parser.add_argument("input", type=str, help="The puzzle input.")
    parser.add_argument(
        "steps",
        type=int,
        default=100,
        nargs="?",
        help="The number of steps.  (default: %(default)s)",
    )
    parser.add_argument(
        "--show", action="store_true", help="Show intermediate steps.  (default: %(default)s)"
    )
    args = parser.parse_args()

    try:
        lines: List[str] = []
        with open(args.input) as inf:
            for line in inf:
                lines.append(line.strip())
        board: Board = Board(lines)
        print(solve(args.steps, board, args.show))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
