# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from itertools import combinations
from typing import List, Tuple


def solve(expenses: List[int], goal: int) -> Tuple[int, int]:
    one: int = None
    for (lhs, rhs) in combinations(expenses, 2):
        if (lhs + rhs) == goal:
            one = lhs * rhs
            break

    two: int = None
    for (x, y, z) in combinations(expenses, 3):
        if (x + y + z) == goal:
            two = x * y * z

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2020 - Day 1 - Report Repair.")
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    parser.add_argument(
        "goal",
        type=int,
        default=2020,
        nargs="?",
        help="The summand to find.  (Default %(default)s)",
    )
    args = parser.parse_args()

    expenses: List[int] = []
    with open(args.input, "rt") as inf:
        for line in inf:
            parts = line.strip().split("-")
            expenses.append(int(line.strip()))
    expenses.sort()

    try:
        print(solve(expenses, args.goal))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
