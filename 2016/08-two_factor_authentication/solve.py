# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from typing import List, Tuple


class Bitmap:
    def __init__(self, rows: int, columns: int):
        self.rows = rows
        self.columns = columns
        self.bits = [False] * (rows * columns)

    def __repr__(self) -> str:
        return f"Bitmap(rows={self.rows}, columns={self.columns})"

    def __str__(self) -> str:
        bmp: List[str] = []
        for row in range(self.rows):
            for column in range(self.columns):
                if self.bits[row * self.columns + column]:
                    bmp.append("#")
                else:
                    bmp.append(".")
            bmp.append("\n")
        return "".join(bmp)

    def count_lit(self) -> int:
        count: int = 0
        for bit in self.bits:
            if bit:
                count += 1
        return count

    def process_command(self, cmd: str) -> None:
        if cmd.startswith("rect "):
            # rect <width>x<height>
            _, rect = cmd.split()
            width, height = rect.split("x")
            self.rect(int(height), int(width))
        elif cmd.startswith("rotate row y="):
            # rotate row y=<row> by <count>
            _, part = cmd.split("=")
            row, count = part.split(" by ")
            self.rotate_row(int(row), int(count))
        elif cmd.startswith("rotate column x="):
            # rotate column x=<column> by <count>
            _, part = cmd.split("=")
            column, count = part.split(" by ")
            self.rotate_column(int(column), int(count))
        else:
            raise ValueError(f"invalid command '{cmd}'")

    def rect(self, height: int, width: int) -> None:
        for row in range(height):
            for column in range(width):
                self.bits[row * self.columns + column] = True

    def rotate_column(self, column: int, count: int) -> None:
        for _ in range(count):
            saved_bit: bool = self.bits[(self.rows - 1) * self.columns + column]
            for row in range(self.rows - 1, 0, -1):
                self.bits[row * self.columns + column] = self.bits[
                    (row - 1) * self.columns + column
                ]
            self.bits[column] = saved_bit

    def rotate_row(self, row: int, count: int) -> None:
        row_offset: int = row * self.columns
        for _ in range(count):
            saved_bit: bool = self.bits[row_offset + self.columns - 1]
            for column in range(self.columns - 1, 0, -1):
                self.bits[row_offset + column] = self.bits[row_offset + column - 1]
            self.bits[row_offset] = saved_bit


def solve(commands: List[str], verbose=False) -> Tuple[int, int]:
    bmp: Bitmap = Bitmap(6, 50)
    if verbose:
        print(f"* initial state\n{bmp}")
    for command in commands:
        bmp.process_command(command)
        if verbose:
            print(f"\n* {command}\n{bmp}")

    one: int = bmp.count_lit()
    two: int = 0
    print(f"** part two:\n{bmp}")

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2016 - Day 8 - Two-Factor Authentication."
    )
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Display extra info.  (Default: %(default)s)",
    )
    args = parser.parse_args()

    commands: List[str] = []
    with open(args.input) as inf:
        for line in inf:
            commands.append(line.strip())

    try:
        print(solve(commands, verbose=args.verbose))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
