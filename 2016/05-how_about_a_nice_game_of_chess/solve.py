# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from hashlib import md5
from typing import List, Tuple


def solve(door_id: str, verbose=False) -> Tuple[str, str]:
    pword_one: List[str] = []
    pword_two: List[str] = [None] * 8  # type: ignore
    chars_left: int = 8
    index: int = 0
    while True:
        digest = md5(bytearray(door_id + str(index), "utf-8")).hexdigest()
        if digest.startswith("00000"):
            if len(pword_one) < 8:
                ch: str = digest[5]
                pword_one.append(ch)
                if verbose:
                    print(f"one: {index} {ch} {pword_one}")
            if chars_left:
                pos: str = digest[5]
                ch = digest[6]
                if pos >= "0" and pos <= "7":
                    position = ord(pos) - ord("0")
                    if not pword_two[position]:
                        pword_two[position] = ch
                        chars_left -= 1
                        if verbose:
                            print(f"two: {index} {pos} '{ch}' {pword_two}")
            if len(pword_one) == 8 and not chars_left:
                break
        index += 1
    one: str = "".join(pword_one)
    two: str = "".join(pword_two)

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2016 - Day 5 - How About a Nice Game of Chess?"
    )
    parser.add_argument(
        "door_id",
        type=str,
        default="ffykfhsq",
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
        print(solve(args.door_id, verbose=args.verbose))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
