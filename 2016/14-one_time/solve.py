# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import pdb
import traceback
from hashlib import md5
from typing import Dict, Optional, Tuple

VERBOSE: bool = False


def memoize(f):
    cache: Dict[Tuple[int, str], str] = {}

    def helper(salt: str, index: int):
        if (index, salt) not in cache:
            cache[(index, salt)] = f(salt, index)
        return cache[(index, salt)]

    return helper


@memoize
def get_digest(salt: str, index: int) -> str:
    return md5(bytearray(salt + str(index), "utf-8")).hexdigest()


@memoize
def get_stretched(salt: str, index: int) -> str:
    digest = md5(bytearray(salt + str(index), "utf-8")).hexdigest()
    for _ in range(2016):
        digest = md5(bytearray(digest, "utf-8")).hexdigest()
    return digest


def three_in_a_row(text: str) -> Optional[str]:
    for idx in range(0, len(text) - 2):
        if text[idx] == text[idx + 1] and text[idx + 1] == text[idx + 2]:
            return text[idx]
    return None


def five_in_a_row(text: str, repch: str) -> bool:
    goal: str = repch * 5
    return text.find(goal) != -1


def is_key(salt: str, index: int) -> bool:
    repch = three_in_a_row(get_digest(salt, index))
    if repch:
        for sub_index in range(index + 1, index + 1001):
            if five_in_a_row(get_digest(salt, sub_index), repch):
                return True
    return False


def is_key2(salt: str, index: int) -> bool:
    repch = three_in_a_row(get_stretched(salt, index))
    if repch:
        for sub_index in range(index + 1, index + 1001):
            if five_in_a_row(get_stretched(salt, sub_index), repch):
                return True
    return False


def solve(salt: str) -> Tuple[int, int]:
    if VERBOSE:
        print(f"salt: {salt}")

    one: int = -1
    index: int = 0
    found: int = 0
    goal: int = 64
    while found < goal:
        if is_key(salt, index):
            found += 1
            if VERBOSE:
                print(f"key {found} found at index {index}")
            one = index
        index += 1

    two: int = -1
    index = 0
    found = 0
    goal = 64
    while found < goal:
        if is_key2(salt, index):
            found += 1
            if VERBOSE:
                print(f"key {found} found at index {index}")
            two = index
        index += 1

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2016 - Day 14 - One-Time Pad.")
    parser.add_argument(
        "salt",
        type=str,
        default="ahsbgdzn",
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

    try:
        print(solve(args.salt))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
