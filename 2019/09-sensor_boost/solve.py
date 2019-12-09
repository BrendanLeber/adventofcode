# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from typing import List, Tuple

from intcode import Intcode


def solve(program: List[int]) -> Tuple[int, int]:
    vm: Intcode = Intcode(program)
    one: int = vm.execute()  # type: ignore

    vm = Intcode(program)
    two: int = vm.execute()  # type: ignore

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2019 - Day 9 - Sensor Boost.")
    parser.add_argument(
        "input",
        type=str,
        default="boost.int",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    args = parser.parse_args()

    program: List[int] = []
    with open(args.input) as inf:
        for line in inf:
            program += list(map(int, line.strip().split(",")))
    try:
        print(solve(program))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
