# -*- coding: utf-8 -*-
"""Advent of Code 2020 - Day 5 - Binary Boarding."""

from __future__ import annotations

import argparse
import pdb
import traceback
from typing import Any, Iterable, List, Tuple


def parse_input(fname: str) -> List[str]:
    """Read the input file and return the parsed data."""
    data: List[str] = []
    with open(fname, "rt") as inf:
        for line in inf:
            data.append(line.strip())
    return data


def determine_seat_id(boardingpass: str) -> int:
    rows: List[int] = [0, 127]  # rows that can be assigned
    aisles: List[int] = [0, 7]  # aisles that can be assigned
    mid: int = 0
    for segment in boardingpass:
        if segment == "F":  # take the front half of rows
            mid = rows[0] + (rows[1] - rows[0]) // 2
            rows[1] = mid
        elif segment == "B":  # take the back half of rows
            mid = rows[0] + (rows[1] - rows[0]) // 2 + 1
            rows[0] = mid
        elif segment == "L":  # take the left half of aisles
            mid = aisles[0] + (aisles[1] - aisles[0]) // 2
            aisles[1] = mid
        elif segment == "R":  # take the right half of aisles
            mid = aisles[0] + (aisles[1] - aisles[0]) // 2 + 1
            aisles[0] = mid
    seat_id: int = rows[0] * 8 + aisles[0]
    return seat_id


def pairwise(iterable: Iterable[Any]) -> Iterable[Tuple[Any, Any]]:
    """s -> (s0, s1), (s2, s3), (s4, s5), ..."""
    itr = iter(iterable)
    return zip(itr, itr)


def solve(boardingpasses: List[str]) -> Tuple[int, int]:
    seat_ids: List[int] = []
    for boardingpass in boardingpasses:
        seat_id: int = determine_seat_id(boardingpass)
        seat_ids.append(seat_id)
    one: int = max(seat_ids)

    # make magic happen
    two: int = -1
    for (lhs, rhs) in pairwise(sorted(seat_ids)):
        if abs(lhs - rhs) > 1:
            two = lhs + 1
            break

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2020 - Day 5 - Binary Boarding.")
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    args = parser.parse_args()

    try:
        data: List[str] = parse_input(args.input)
        print(solve(data))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
