# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from functools import reduce
from itertools import combinations
from operator import mul
from typing import List, Tuple


def findqe(weights: List[int], num_groups) -> int:
    goal_weight = sum(weights) // num_groups
    start = 0
    end = int(len(weights) / num_groups) + 2
    for i in range(start, end):
        qes = [reduce(mul, c) for c in combinations(weights, i) if sum(c) == goal_weight]
        if qes:
            return min(qes)
    return -1


def solve(weights: List[int], verbose=False) -> Tuple[int, int]:
    one: int = findqe(weights, 3)
    two: int = findqe(weights, 4)
    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2015 - Day 24 - It Hangs in the Balance."
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

    weights: List[int] = []
    with open(args.input) as inf:
        for line in inf:
            weights.append(int(line.strip()))

    try:
        print(solve(weights, verbose=args.verbose))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
