# -*- coding: utf-8 -*-
"""Advent of Code 2020 - Day 14 - Docking Data."""

import argparse
import pdb
import re
import traceback


def apply_mask(value, mask):
    for bit, op in enumerate(mask):
        if op == "X":
            continue
        bitmask = 2 ** bit
        if op == "0":
            value &= ~bitmask
        else:
            value |= bitmask
    return value & 2 ** 36 - 1


def fork(mask):
    if "X" not in mask:
        return [int(mask, 2)]
    x = mask.find("X")
    return fork(mask[:x] + "0" + mask[x + 1 :]) + fork(mask[:x] + "1" + mask[x + 1 :])


def parse_addr(line):
    m = re.match(r"^mem\[(\d+)\]\s+=\s+(\d+)$", line)
    return (int(m[1]), int(m[2]))


def solve_one(inits):
    memory = {}
    mask = []
    for cmd in inits:
        if cmd.startswith("mask"):
            m = re.match(r"^mask\s+=\s+([X10]+)$", cmd)
            mask = list(reversed(m[1]))
        elif cmd.startswith("mem"):
            addr, value = parse_addr(cmd)
            memory[addr] = apply_mask(value, mask)
    return sum(memory.values())


def solve_two(inits):
    memory = {}
    mask = ""
    for cmd in inits:
        if cmd.startswith("mask"):
            m = re.match(r"^mask\s+=\s+([X10]+)$", cmd)
            mask = m[1]
        elif cmd.startswith("mem"):
            addr, value = parse_addr(cmd)
            addr = f"{addr:036b}"

            adjusted = []
            for m, a in zip(mask, addr):
                if m in "1X":
                    adjusted.append(m)
                else:
                    adjusted.append(a)

            forks = fork("".join(adjusted))
            for f in forks:
                memory[f] = value
    return sum(memory.values())


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2020 - Day 14 - Docking Data.")
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    args = parser.parse_args()

    try:
        with open(args.input, "rt") as inf:
            inits = inf.readlines()

        print((solve_one(inits), solve_two(inits)))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
