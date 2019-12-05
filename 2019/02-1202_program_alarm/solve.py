# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from typing import List, Optional, Tuple

from intcode import Intcode

VERBOSE: bool = False


def solve(program: List[int]) -> Tuple[Optional[int], Optional[int]]:
    vm: Intcode = Intcode(program)
    vm.reset()
    vm.set_noun_and_verb(12, 2)
    one: Optional[int] = vm.execute()

    for noun in range(100):
        for verb in range(100):
            if VERBOSE:
                print(f"Testing noun {noun} and verb {verb}.")
            vm.reset()
            vm.set_noun_and_verb(noun, verb)
            output: Optional[int] = vm.execute()
            if output == 19690720:
                two: Optional[int] = 100 * noun + verb
                return (one, two)

    return (one, None)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2019 - Day 2 - 1202 Program Alarm."
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
    VERBOSE = args.verbose

    program: List[int] = []
    with open(args.input) as inf:
        for line in inf:
            program += list(map(int, line.strip().split(",")))
    try:
        print(solve(program))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
