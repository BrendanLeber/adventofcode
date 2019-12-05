#!/usr/bin/env python3


import argparse
import pdb
import traceback
from typing import Tuple


def solve(data: str) -> Tuple[int, int]:
    # start on the ground floor
    floor: int = 0

    # which character caused us to enter the basement
    pos: int = 0
    found_basement: bool = False
    basement_pos: int = 0

    for order in data:
        pos = pos + 1

        if order == "(":
            floor = floor + 1
        elif order == ")":
            floor = floor - 1
        else:
            raise ValueError("invalid character {0} in puzzle data".format(order))

        if not found_basement and floor == -1:
            found_basement = True
            basement_pos = pos

    return (floor, basement_pos)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2015 - Day 1 - Not Quite Lisp.")
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
    VERBOSE = args.verbose

    try:
        with open(args.input, "rt") as inf:
            for line in inf:
                puzzle = line.strip()
        print(solve(puzzle))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
