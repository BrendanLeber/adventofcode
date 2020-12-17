# -*- coding: utf-8 -*-
"""Advent of Code 2020 - Day 15 - Rambunctious Recitation."""

import argparse
import pdb
import traceback
from re import findall


def extract_ints(line):
    return [int(x) for x in findall(r"-?\d+", line)]


def find_offsets(values, target):
    offsets = []
    for idx, value in enumerate(values):
        if value == target:
            offsets.append(idx)
    return offsets


def solve(numbers, limit):
    last = {}
    for i, x in enumerate(numbers[:-1]):
        last[x] = i
    seen = numbers[-1]
    for i in range(len(numbers) - 1, limit - 1):
        x = i - last[seen] if seen in last else 0
        last[seen] = i
        seen = x
    return seen


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2020 - Day 15 - Rambunctious Recitation."
    )
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    args = parser.parse_args()

    try:
        numbers = []
        with open(args.input, "rt") as inf:
            for line in inf:
                numbers += extract_ints(line)

        print((solve(numbers, 2020), solve(numbers, 30_000_000)))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
