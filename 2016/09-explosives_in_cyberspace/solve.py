# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from typing import Tuple


def decompress(text: str) -> int:
    length: int = 0
    start: int = 0
    end: int = 0
    while start < len(text):
        if text[start] != "(":
            end = text.find("(", start)
            if end == -1:
                length += len(text) - start
                return length
            else:
                length += end - start
                start = end
        else:
            end = text.find(")", start)
            marker: str = text[start + 1:end]
            num_chars, num_repeat = parse_marker(marker)
            length += num_repeat * num_chars
            start = end + num_chars + 1

    return length


def decompress2(text: str) -> int:
    length: int = 0
    start: int = 0
    end: int = 0
    while start < len(text):
        if text[start] != "(":
            end = text.find("(", start)
            if end == -1:
                length += len(text) - start
                return length
            else:
                length += end - start
                start = end
        else:
            end = text.find(")", start)
            marker: str = text[start + 1:end]
            num_chars, num_repeat = parse_marker(marker)
            sub: str = text[start + len(marker) + 2:start + len(marker) + 2 + num_chars]
            length += num_repeat * decompress2(sub)
            start = end + num_chars + 1

    return length


def parse_marker(marker: str) -> Tuple[int, int]:
    num_chars, num_repeat = marker.split("x")
    return (int(num_chars), int(num_repeat))


def solve(ctext: str, verbose=False) -> Tuple[int, int]:
    if verbose:
        print(f"compressed: {ctext}")

    one: int = decompress(ctext)
    two: int = decompress2(ctext)

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2016 - Day 9 - Explosives in Cyberspace."
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

    try:
        with open(args.input) as inf:
            for line in inf:
                print(solve(line.strip(), verbose=args.verbose))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
