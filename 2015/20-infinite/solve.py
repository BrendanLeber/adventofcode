# -*- coding: utf-8 -*-

import argparse
import math
import pdb
import traceback
from typing import List, Tuple


def get_divisors(n: int) -> List[int]:
    small = [i for i in range(1, int(math.sqrt(n)) + 1) if n % i == 0]
    large = [n // d for d in small if n != d * d]
    return small + large


def solve(target: int) -> Tuple[int, int]:
    one = two = None
    i: int = 1
    while not one or not two:
        i += 1
        divisors = get_divisors(i)
        if not one:
            if sum(divisors) * 10 >= target:
                one = i
        if not two:
            if sum(d for d in divisors if i / d <= 50) * 11 >= target:
                two = i
    return (one, two)


def slow(target: int) -> Tuple[int, int]:
    one = two = -1
    houses: List[int] = [0] * (target + 1)
    for elf in range(1, target):
        for house in range(elf, target, elf):
            houses[house] += elf * 10

    for house, gifts in enumerate(houses):
        if gifts >= target:
            one = house

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2015 - Day 20 - Infinite Elves and Infinite Houses."
    )
    parser.add_argument(
        "input",
        type=int,
        default=33100000,
        nargs="?",
        help="The puzzle input.  (Default: %(default)s)",
    )
    args = parser.parse_args()

    try:
        print(solve(args.input))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
