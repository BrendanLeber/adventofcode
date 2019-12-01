# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import pdb
import traceback
from typing import List, Tuple

VERBOSE: bool = False


def checksum(data: str) -> str:
    def _check(d: str) -> str:
        res: str = ""
        for p in [(d[i:i + 2]) for i in range(0, len(d), 2)]:
            if p in ["00", "11"]:
                res += "1"
            elif p in ["01", "10"]:
                res += "0"
        if VERBOSE:
            print(f"{res} {len(res)}")
        return res

    result: str = _check(data)
    while not (len(result) & 1):
        result = _check(result)
    return result


def dragon(a: str) -> str:
    result: str = a + "0"
    for bit in reversed(a):
        result += "1" if bit == "0" else "0"
    return result


def generate_data(size: int, initial: str) -> str:
    data = initial
    while len(data) < size:
        data = dragon(data)
        if VERBOSE:
            print(f"{len(data)} {data}")
    return data[:size]


def solve(disk_sizes: Tuple[int, int], initial_state: str) -> Tuple[str, str]:
    if VERBOSE:
        print(f"   disk sizes: {disk_sizes}")
        print(f"initial state: {initial_state}")

    data = generate_data(disk_sizes[0], initial_state)
    if VERBOSE:
        print(f"data: {len(data)} {data}")
    one: str = checksum(data)
    if VERBOSE:
        print(f"checksum: {one} {len(one)}")

    data = generate_data(disk_sizes[1], initial_state)
    if VERBOSE:
        print(f"data: {len(data)} {data}")
    two: str = checksum(data)
    if VERBOSE:
        print(f"checksum: {two} {len(two)}")

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2016 - Day 16 - Dragon Checksum")
    parser.add_argument(
        "initial",
        type=str,
        default="01111010110010011",
        nargs="?",
        help="The initial state of data.  (Default %(default)s)",
    )
    parser.add_argument(
        "size1",
        type=int,
        default=272,
        nargs="?",
        help="The size of first disk.  (Default %(default)s)",
    )
    parser.add_argument(
        "size2",
        type=int,
        default=35651584,
        nargs="?",
        help="The size of second disk.  (Default %(default)s)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Display extra info.  (Default: %(default)s)",
    )
    args = parser.parse_args()
    VERBOSE = args.verbose

    try:
        print(solve((args.size1, args.size2), args.initial))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
