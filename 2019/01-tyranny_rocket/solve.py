# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from typing import List, Tuple

VERBOSE: bool = False


def solve(masses: List[int]) -> Tuple[int, int]:
    one: int = 0
    for mass in masses:
        fuel = mass // 3 - 2
        one += fuel
        if VERBOSE:
            print(f"{mass} {fuel} {one}")

    two: int = 0
    for mass in masses:
        module_fuel = mass // 3 - 2
        fuel = 0
        while module_fuel > 0:
            fuel += module_fuel
            module_fuel = module_fuel // 3 - 2
        two += fuel
        if VERBOSE:
            print(f"{mass} {fuel} {two}")

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2019 - Day 1 - The Tyranny of the Rocket Equation."
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
    VERBOSE = args.verbose

    masses: List[int] = []
    with open(args.input) as inf:
        for line in inf:
            masses.append(int(line.strip()))
    try:
        print(solve(masses))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
