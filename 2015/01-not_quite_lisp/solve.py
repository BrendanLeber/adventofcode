#!/usr/bin/env python3


import fileinput
import pdb
import traceback
from typing import Tuple


def solve(data) -> Tuple[int, int]:
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
    try:
        for line in fileinput.input():
            puzzle = line.strip()
            print(solve(puzzle))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
