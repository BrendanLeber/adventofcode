#!/usr/bin/env python3
"""
Solve the Advent of Code Day 01 problem:
'Not Quite Lisp'.
"""


import fileinput


def solve(data):
    """Solve parts one and two."""

    # start on the ground floor
    floor = 0

    # which character caused us to enter the basement
    pos = 0
    found_basement = False
    basement_pos = 0

    for order in data:
        pos = pos + 1

        if order == "(":
            floor = floor + 1
        elif order == ")":
            floor = floor - 1
        else:
            raise ValueError("invalid character {0} in puzzle data".format(order))

        if not found_basement and floor == -1:
            found_basement = True
            basement_pos = pos

    return (floor, basement_pos)


if __name__ == "__main__":
    # read problem input from file or stdin
    puzzle = ""
    for line in fileinput.input():
        puzzle = puzzle + line.strip()

    result = solve(puzzle)
    print(result)
