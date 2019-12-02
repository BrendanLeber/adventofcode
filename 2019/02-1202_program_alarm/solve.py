# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from copy import copy
from itertools import permutations
from typing import List, Optional, Tuple

VERBOSE: bool = False


def execute(noun: int, verb: int, pgm: List[int]) -> Optional[int]:
    ram: List[int] = copy(pgm)
    ram[1] = noun
    ram[2] = verb
    ip: int = 0
    while ram[ip] != 99:  # halt
        if ram[ip] == 1:  # add
            ram[ram[ip + 3]] = ram[ram[ip + 1]] + ram[ram[ip + 2]]
            ip += 4
        elif ram[ip] == 2:  # mul
            ram[ram[ip + 3]] = ram[ram[ip + 1]] * ram[ram[ip + 2]]
            ip += 4
        else:
            return None
    return ram[0]


def solve(program: List[int]) -> Tuple[Optional[int], int]:
    noun: int = 12  # restore gravity assist
    verb: int = 2
    one: Optional[int] = execute(noun, verb, program)

    nouns_and_verbs: List[int] = list(range(100)) + list(range(100))
    for noun, verb in permutations(nouns_and_verbs, 2):
        output: Optional[int] = execute(noun, verb, program)
        if output == 19690720:
            break
    two: int = 100 * noun + verb

    return (one, two)


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
