# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple


@dataclass
class Instruction:
    name: str
    reg: Optional[str]
    offset: Optional[int]

    def __str__(self) -> str:
        if self.name in ["hlf", "tpl", "inc"]:
            return f"{self.name} {self.reg}"
        elif self.name in ["jie", "jio"]:
            return f"{self.name} {self.reg}, {self.offset}"
        elif self.name in ["jmp"]:
            return f"{self.name} {self.offset}"
        else:
            raise ValueError(f"Unkown instruction: {self.name}")


def execute(program: List[Instruction], regs: Dict[str, int], verbose=False) -> Dict[str, int]:
    ip: int = 0
    while True:
        if ip >= len(program):
            break

        inst = program[ip]
        if verbose:
            print(f"{ip:05d}: {inst!s} {regs}")

        if inst.name == "hlf":  # half r
            regs[inst.reg] = regs[inst.reg] // 2
            ip += 1
        elif inst.name == "tpl":  # triple r
            regs[inst.reg] = regs[inst.reg] * 3
            ip += 1
        elif inst.name == "inc":  # increment r
            regs[inst.reg] = regs[inst.reg] + 1
            ip += 1
        elif inst.name == "jmp":  # jump
            ip += inst.offset
        elif inst.name == "jie":  # jump if r is even
            if regs[inst.reg] % 2 == 0:
                ip += inst.offset
            else:
                ip += 1
        elif inst.name == "jio":  # jump if r is one
            if regs[inst.reg] == 1:
                ip += inst.offset
            else:
                ip += 1

    if verbose:
        print(f"final state: ip:{ip} regs:{regs}")

    return regs


def solve(program: List[Instruction], verbose=False) -> Tuple[int, int]:
    regs: Dict[str, int] = {"a": 0, "b": 0}
    regs = execute(program, regs, verbose)
    one = regs["b"]

    regs: Dict[str, int] = {"a": 1, "b": 0}
    regs = execute(program, regs, verbose)
    two = regs["b"]

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2015 - Day 23 - Opening the Turing Lock."
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

    program: List[Instruction] = []
    with open(args.input) as inf:
        for line in inf:
            parts = line.strip().split()
            if parts[0] in ["inc", "tpl", "hlf"]:
                inst = Instruction(parts[0], parts[1], None)
            elif parts[0] in ["jie", "jio"]:
                inst = Instruction(parts[0], parts[1][0], int(parts[2]))
            elif parts[0] in ["jmp"]:
                inst = Instruction(parts[0], None, int(parts[1]))
            else:
                raise ValueError("unknown instruction '{line.strip()}'")
            program.append(inst)

    try:
        print(solve(program, verbose=args.verbose))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
