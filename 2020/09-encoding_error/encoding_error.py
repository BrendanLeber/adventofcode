# -*- coding: utf-8 -*-
"""Advent of Code 2020 - Day 9 - Encoding Error."""

import argparse
import pdb
import traceback
from itertools import combinations
from typing import Any, List, Set, Tuple


def parse_input(fname: str):
    """Read the input file and return the parsed data."""
    data = []
    with open(fname, "rt") as inf:
        for line in inf:
            data.append(int(line.strip()))
    return data


def get_sums(slice: List[int]) -> Set[int]:
    result: Set[int] = set()
    for (lhs, rhs) in combinations(slice, 2):
        result.add(lhs + rhs)
    return result


def check_window(target: int, numbers: List[int], sz: int) -> Tuple[bool, Any]:
    for x in range(len(numbers) - sz + 1):
        window: List[int] = numbers[x : x + sz]
        if sum(window) == target:
            return (True, min(window) + max(window))
    return (False, None)


def solve(numbers: List[int], preamble: int):
    one = None
    for idx in range(preamble, len(numbers)):
        start: int = idx - preamble
        end: int = idx
        sums: Set[int] = get_sums(numbers[start:end])
        if numbers[idx] not in sums:
            one = numbers[idx]
            break

    two = None
    window_size: int = 1
    while True:
        window_size += 1
        found, two = check_window(one, numbers, window_size)
        if found:
            break

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2020 - Day 9 - Encoding Error.")
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    parser.add_argument(
        "preamble",
        type=int,
        default=25,
        nargs="?",
        help="The number of items in the preamble.  (Default %(default)s)",
    )
    args = parser.parse_args()

    try:
        data = parse_input(args.input)
        print(solve(data, args.preamble))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
