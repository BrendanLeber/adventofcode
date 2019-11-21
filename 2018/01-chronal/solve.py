# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from typing import List, Set, Tuple


def solve(frequency_changes: List[int]) -> Tuple[int, int]:
    one = sum(frequency_changes)

    two = None
    frequency: int = 0
    frequencies_found: Set[int] = set()
    frequencies_found.add(frequency)
    while not two:
        print("while loop")
        for change in frequency_changes:
            frequency += change
            if frequency in frequencies_found:
                two = frequency
                break
            frequencies_found.add(frequency)

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2018 - Day 1 - Chronal Calibration."
    )
    parser.add_argument("input", type=str, help="The puzzle input.")
    args = parser.parse_args()

    try:
        frequency_changes: List[int] = []
        with open(args.input) as inf:
            for line in inf:
                frequency_changes.append(int(line))
        print(solve(frequency_changes))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
