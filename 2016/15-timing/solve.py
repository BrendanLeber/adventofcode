# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import pdb
import traceback
from copy import deepcopy
from dataclasses import dataclass
from typing import List, Tuple

VERBOSE: bool = False


@dataclass
class Disc:
    n: int
    time: int
    positions: int
    position: int

    def spin(self, steps: int = 1) -> None:
        self.time += steps
        self.position = (self.position + steps) % self.positions

    def __str__(self) -> str:
        return (
            f"Disc #{self.n} has"
            f" {self.positions} positions;"
            f"at time={self.time},"
            f"it is at position {self.position}."
        )


def run_simulation(discs: List[Disc]) -> int:
    if VERBOSE:
        print("Disc Starting Positions:")
        for disc in discs:
            print(disc)

    time: int = 0
    for tick, disc in enumerate(discs):
        disc.spin(time + tick + 1)

    if VERBOSE:
        print(f"\nAt time {time} the disks positions are:")
        for disc in discs:
            print(disc)

    while True:
        if all([d.position == 0 for d in discs]):
            return time

        time += 1
        for disc in discs:
            disc.spin()

        if VERBOSE:
            print(f"\nAt time {time} the disks positions are:")
            for disc in discs:
                print(disc)


def solve(discs: List[Disc]) -> Tuple[int, int]:
    one: int = run_simulation(deepcopy(discs))

    discs.append(Disc(n=discs[-1].n + 1, time=0, positions=11, position=0))

    two: int = run_simulation(discs)
    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2016 - Day 15 - Timing is Everything."
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

    discs: List[Disc] = []
    with open(args.input, "rt") as inf:
        for line in inf:
            parts = line.strip().split()
            discs.append(
                Disc(
                    n=int(parts[1][1:]),
                    positions=int(parts[3]),
                    time=int(parts[6][5:-1]),
                    position=int(parts[11][:-1]),
                )
            )

    try:
        print(solve(discs))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
