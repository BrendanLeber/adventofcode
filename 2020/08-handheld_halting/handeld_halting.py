# -*- coding: utf-8 -*-
"""Advent of Code 2020 - Day 8 - Handheld Halting."""

import argparse
import pdb
import traceback


def parse_input(fname: str):
    """Read the input file and return the parsed data."""
    data = []
    with open(fname, "rt") as inf:
        for line in inf:
            (op, arg) = line.strip().split()
            data.append((op, int(arg)))
    return data


class CPU:
    def __init__(self, program):
        self.original = program[:]
        self.reset()

    def reset(self):
        self.ram = self.original[:]
        self.seen = set()
        self.acc = 0
        self.ip = 0

    def run(self):
        good = False
        while True:
            if self.ip == len(self.ram):
                good = True
                break

            if self.ip in self.seen or not 0 <= self.ip < len(self.ram):
                break

            self.seen.add(self.ip)

            (op, arg) = self.ram[self.ip]
            if op == "acc":
                self.acc += arg
                self.ip += 1
            elif op == "jmp":
                self.last_jmp_ip = self.ip
                self.ip += arg
            elif op == "nop":
                self.ip += 1

        return (self.acc, good)


def solve(pgm):
    cpu = CPU(pgm)
    (one, _) = cpu.run()

    two = 0
    for fix in range(len(cpu.ram)):
        cpu.reset()
        (op, value) = cpu.ram[fix]
        if op == "acc":
            continue
        elif op == "jmp":
            cpu.ram[fix] = ("nop", value)
        else:
            cpu.ram[fix] = ("jmp", value)
        (two, good) = cpu.run()
        if good:
            break

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2020 - Day 8 - Handheld Halting."
    )
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    args = parser.parse_args()

    try:
        data = parse_input(args.input)
        print(solve(data))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
