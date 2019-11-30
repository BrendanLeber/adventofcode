# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from typing import Dict, List, Tuple

VERBOSE: bool = False


def execute(program: List[Tuple[str, ...]], regs: Dict[str, int]) -> Dict[str, int]:
    ip: int = 0
    while True:
        if ip >= len(program):
            break

        op = program[ip]
        if VERBOSE:
            print(f"{ip:05d}: {op} {regs}")

        if op[0] == "cpy":  # cpy x y
            if isinstance(op[1], str):
                value = regs[op[1]]
            else:
                value = op[1]
            regs[op[2]] = value
            ip += 1
        elif op[0] == "inc":  # inc x
            regs[op[1]] += 1
            ip += 1
        elif op[0] == "dec":  # dec x
            regs[op[1]] -= 1
            ip += 1
        elif op[0] == "jnz":  # jnz x y
            if isinstance(op[1], str):
                value = regs[op[1]]
            else:
                value = op[1]
            if isinstance(op[2], str):
                offset = regs[op[2]]
            else:
                offset = op[2]
            if value != 0:
                ip += offset
            else:
                ip += 1

    if VERBOSE:
        print(f"final state: ip:{ip} regs:{regs}")

    return regs


def parse_instruction(instruction: str) -> Tuple[str, ...]:
    parts = instruction.split()
    if parts[0] in ["inc", "dec"]:
        # (instruction, register)
        return (parts[0], parts[1])
    elif parts[0] in ["cpy", "jnz"]:
        # (instruction, (register|integer), (register|integer)
        inst, ria, rib = parts
        if ria.isdigit() or ria[0] == "-":
            ria = int(ria)
        if rib.isdigit() or rib[0] == "-":
            rib = int(rib)
        return (inst, ria, rib)
    else:
        raise ValueError(f"invalid instruction '{instruction}'")


def solve(program: List[Tuple[str, ...]]) -> Tuple[int, int]:
    regs: Dict[str, int] = {"a": 0, "b": 0, "c": 0, "d": 0}
    regs = execute(program, regs)
    one: int = regs["a"]

    regs = {"a": 0, "b": 0, "c": 1, "d": 0}
    regs = execute(program, regs)
    two: int = regs["a"]

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2016 - Day 12 - Leonardo's Monorail."
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

    program: List[Tuple[str, ...]] = []
    with open(args.input) as inf:
        for line in inf:
            program.append(parse_instruction(line.strip()))
    try:
        print(solve(program))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
