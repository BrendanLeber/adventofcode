# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from itertools import combinations
from math import prod
from typing import List, Tuple


def find_matching_sum(values: List[int], goal: int, k: int) -> Tuple[int, ...]:
    for trie in combinations(values, k):
        if sum(trie) == goal:
            return trie
    return ()


def solve(expenses: List[int], goal: int) -> Tuple[int, int]:
    one: int = prod(find_matching_sum(expenses, goal, 2))
    two: int = prod(find_matching_sum(expenses, goal, 3))
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
