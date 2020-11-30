# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from typing import List, Tuple


def is_trap(test_case: str) -> bool:
    if test_case in ["^^.", ".^^", "^..", "..^"]:
        return True
    return False


def generate_field(initial_row: str, num_rows: int) -> int:
    safe_tiles = initial_row.count(".")
    current_row = initial_row
    for line in range(1, num_rows):
        new_row = ""
        # handle left edge, pos 0
        new_row += "^" if is_trap(f".{current_row[0]}{current_row[1]}") else "."
        # handle the middles
        for pos in range(1, len(current_row) - 1):
            new_row += "^" if is_trap(current_row[pos - 1 : pos + 2]) else "."
        # handle right edge
        new_row += "^" if is_trap(f"{current_row[-2:]}.") else "."
        safe_tiles += new_row.count(".")
        current_row = new_row
    return safe_tiles


def solve(initial_row: str, num_rows: int) -> Tuple[int, int]:
    one: int = generate_field(initial_row, num_rows)
    two: int = generate_field(initial_row, 400000)
    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2016 - Day 18 - Like a Rogue.")
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    parser.add_argument(
        "rows",
        type=int,
        default=40,
        nargs="?",
        help="The number of rows to generate.  (Default %(default)s)",
    )
    args = parser.parse_args()

    with open(args.input, "rt") as inf:
        lines = inf.read().splitlines()

    try:
        print(solve(lines[0], args.rows))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
