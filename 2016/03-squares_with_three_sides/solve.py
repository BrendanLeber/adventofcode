# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from typing import List, Tuple

Triangle = Tuple[int, int, int]


def triangle_valid(tri: Triangle) -> bool:
    st = tuple(sorted(tri))
    return st[0] + st[1] > st[2]


def solve(triangles: List[Triangle], verbose=False) -> Tuple[int, int]:
    one: int = 0
    for triangle in triangles:
        if triangle_valid(triangle):
            one += 1

    two: int = 0
    for idx in range(0, len(triangles), 3):
        vt = tuple(sorted((triangles[idx][0], triangles[idx + 1][0], triangles[idx + 2][0])))
        if triangle_valid(vt):
            two += 1

        vt = tuple(sorted((triangles[idx][1], triangles[idx + 1][1], triangles[idx + 2][1])))
        if triangle_valid(vt):
            two += 1

        vt = tuple(sorted((triangles[idx][2], triangles[idx + 1][2], triangles[idx + 2][2])))
        if triangle_valid(vt):
            two += 1

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2016 - Day 3 - Squares with Three Sides."
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

    triangles: List[Triangle] = []
    with open(args.input) as inf:
        for line in inf:
            sides = tuple(map(int, line.strip().split()))
            if len(sides) != 3:
                raise ValueError(f"invalid triangle.  '{line}'")
            triangles.append(sides)

    try:
        print(solve(triangles, verbose=args.verbose))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
