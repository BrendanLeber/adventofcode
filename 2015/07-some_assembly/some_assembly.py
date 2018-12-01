#!/usr/bin/env python
"""
Solve the Advent of Code Day 07 problem:
'Some Assembly Required'.
"""


from collections import namedtuple
from dataclasses import dataclass
import fileinput
import re


Order = namedtuple("Order", ["cmd", "rect"])


def solve_part_1(orders):
    """Solve the first part of the puzzle."""
    return -1


def solve_part_2(orders):
    """Solve the second part of the puzzle."""
    return -1


if __name__ == "__main__":
    orders = []
    for line in fileinput.input():
        orders.append(line.strip())

    print(solve_part_1(orders))
    # print(solve_part_2(orders))
