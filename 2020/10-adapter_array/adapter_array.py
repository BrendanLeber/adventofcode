# -*- coding: utf-8 -*-
"""Advent of Code 2020 - Day 10 - Adapter Array."""

import argparse
import pdb
import traceback
from itertools import combinations
from typing import Any, List, Set, Tuple


def read_adapters(fname: str) -> List[int]:
    with open(fname, "rt") as inf:
        return [0] + list(sorted(map(int, inf.read().splitlines())))


def get_candidates(target: int, joltages: List[int]) -> List[int]:
    results: List[int] = []
    for joltage in joltages:
        if joltage <= target + 3:
            results.append(joltage)
    return results


def solve(adapters: List[int]):
    diffs: Dict[int, int] = { 1: 0, 2: 0, 3: 1}
    for i in range(1, len(adapters)):
        diffs[adapters[i] - adapters[i-1]] += 1
    one = diffs[1] * diffs[3]

    paths = [1] + [0] * (len(adapters) - 1)
    for i, adapter in enumerate(adapters):
        for j in range(i - 3, i):
            if adapter - adapters[j] <= 3:
                paths[i] += paths[j]
    two = paths[-1]

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2020 - Day 10 - Adapter Array.")
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    args = parser.parse_args()

    try:
        data = read_adapters(args.input)
        print(solve(data))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
