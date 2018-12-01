#!/usr/bin/env python3
"""
Solve the Advent of Code Day 04 problem:
'The Ideal Stocking Stuffer'.
"""

from __future__ import print_function
from hashlib import md5
import fileinput
import re
import sys


def eprint(*args, **kwargs):
    """Print to stderr."""
    print(*args, file=sys.stderr, *kwargs)


def solve_part_1(puzzle_data):
    """Solve part one of the puzzle."""
    answer = -1
    pattern = re.compile("^0{5}")
    while True:
        answer += 1
        hasher = md5()
        attempt = puzzle_data + str(answer)
        hasher.update(attempt.encode("utf-8"))
        digest = hasher.hexdigest()
        if re.search(pattern, digest):
            return answer


def solve_part_2(puzzle_data):
    """Solve part two of the puzzle."""
    answer = -1
    pattern = re.compile("^0{6}")
    while True:
        answer += 1
        hasher = md5()
        attempt = puzzle_data + str(answer)
        hasher.update(attempt.encode("utf-8"))
        digest = hasher.hexdigest()
        if re.search(pattern, digest):
            return answer


def solve(puzzle_data):
    """Solve the puzzle."""
    return (solve_part_1(puzzle_data), solve_part_2(puzzle_data))


if __name__ == "__main__":
    # read problem input from file or stdin
    data = ""
    for line in fileinput.input():
        data = data + line.strip()

    print(solve(data))
