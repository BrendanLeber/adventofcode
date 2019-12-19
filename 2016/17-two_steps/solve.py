# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from typing import List, Tuple
from hashlib import md5

VERBOSE: bool = False


def solve(passcode: str) -> Tuple[str, str]:
    if VERBOSE:
        print(f"passcode: {passcode}")

    one: str = None
    two: str = None

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2016 - Day 17 - Two Steps Forward.")
    parser.add_argument(
        "passcode",
        type=str,
        default="hhhxzeay",
        nargs="?",
        help="The vault passcode.  (Default %(default)s)",
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
        print(solve(args.passcode))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
