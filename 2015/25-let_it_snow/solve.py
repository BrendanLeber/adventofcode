# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback


def code(n: int) -> int:
    first_code: int = 20151125
    multiplier: int = 252533
    divisor: int = 33554393

    code = first_code
    for _ in range(1, n):
        code = (code * multiplier) % divisor
    return code


def pos_to_index(row: int, col: int) -> int:
    return sum(range(row + col - 1)) + col


def solve(row: int, col: int, verbose=False) -> int:
    if verbose:
        print(f"row: {row}  column: {col}")

    index = pos_to_index(row, col)
    if verbose:
        print(f"index: {index}")

    one: int = code(index)
    return one


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2015 - Day 25 - Let It Snow.")
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Display extra info.  (Default: %(default)s)",
    )
    args = parser.parse_args()

    try:
        print(solve(2978, 3083, verbose=args.verbose))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
