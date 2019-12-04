# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from collections import OrderedDict
from typing import Dict, List, Tuple

VERBOSE: bool = False


def rle(text: str) -> List[Tuple[str, int]]:
    counts: Dict[str, int] = OrderedDict.fromkeys(text, 0)
    for ch in text:
        counts[ch] += 1
    result: List[Tuple[str, int]] = []
    for k, v in counts.items():
        result.append((k, v))
    return result


def valid_password1(pword: str) -> bool:
    counts: List[Tuple[str, int]] = rle(pword)

    # two adjacent digits are the same
    if not any([c[1] >= 2 for c in counts]):
        return False

    # from left to right the digits must be equal or increase
    for idx in range(0, len(pword) - 1):
        if pword[idx + 1] < pword[idx]:
            return False

    # both rules passed.  it is valid
    return True


def valid_password2(pword: str) -> bool:
    # two adjacent digits are the same,
    # but not part of a larger repeated group
    counts: List[Tuple[str, int]] = rle(pword)
    if not any([c[1] == 2 for c in counts]):
        return False

    # from left to right the digits must be equal or increase
    for idx in range(0, len(pword) - 1):
        if pword[idx + 1] < pword[idx]:
            return False

    # both rules passed.  it is valid
    return True


def solve(start: int, end: int) -> Tuple[int, int]:
    one: int = 0
    two: int = 0
    for password in range(start, end + 1):
        pword: str = str(password)
        if valid_password1(pword):
            one += 1
        if valid_password2(pword):
            two += 1

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2019 - Day 4 - Secure Container."
    )
    parser.add_argument(
        "input",
        type=str,
        default="130254-678275",
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
        parts: List[str] = args.input.split("-")
        start: int = int(parts[0])
        end: int = int(parts[1])
        print(solve(start, end))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
