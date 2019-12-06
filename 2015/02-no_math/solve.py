# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from typing import List, Optional, Tuple

Package = Tuple[int, int, int]
Packages = List[Package]


def solve(packages: Packages) -> Tuple[Optional[int], Optional[int]]:
    total_paper: int = 0
    total_ribbon: int = 0

    for length, width, height in packages:
        faces: List[int] = [width * height, length * height, width * length]
        extra: int = min(faces)

        paper: int = 0
        for face in faces:
            paper += 2 * face
        total_paper += paper + extra

        perimiters: List[int] = [2 * (width + height), 2 * (length + height), 2 * (width + length)]
        wrap: int = min(perimiters)
        bow: int = width * length * height
        total_ribbon += wrap + bow

    return (total_paper, total_ribbon)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2015 - Day 2 - I Was Told There Would Be No Math."
    )
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    args = parser.parse_args()

    puzzle_data: Packages = []
    with open(args.input, "rt") as inp:
        for line in inp:
            l, w, h = list(map(int, line.strip().split("x")))
            puzzle_data.append((l, w, h))

    try:
        print(solve(puzzle_data))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
