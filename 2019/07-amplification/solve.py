# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from itertools import permutations
from typing import List, Tuple

from intcode import Intcode


def solve(program: List[int]) -> Tuple[int, int]:
    phases = (0, 1, 2, 3, 4)
    signals = [0] * (len(phases) + 1)
    results = []
    vms = [Intcode(program) for _ in phases]
    for trie in permutations(phases):
        for idx, phase in enumerate(trie):
            vms[idx].reset()
            vms[idx].set_inputs([phase, signals[idx]])
            while not vms[idx].execute():
                pass
            signals[idx + 1] = vms[idx].last_output
        results.append((trie, signals[-1]))
    one = max([r[1] for r in results])

    phases = (5, 6, 7, 8, 9)
    results = []
    for phase in permutations(phases):
        signals = [0] * (len(phases) + 1)
        more_work = [True] * len(phases)
        vms = [Intcode(program) for _ in phases]

        for idx in range(len(vms)):
            vms[idx].set_inputs([phase[idx], signals[idx]])
            more_work[idx] = vms[idx].execute()
            signals[idx + 1] = vms[idx].last_output
        signals[0] = signals[-1]

        while any(more_work):
            for idx in range(len(vms)):
                if not more_work[idx]:
                    continue
                vms[idx].set_inputs([signals[idx]])
                more_work[idx] = vms[idx].execute()
                signals[idx + 1] = vms[idx].last_output
            signals[0] = signals[-1]

        results.append((phase, signals[-1]))
    two = max([r[1] for r in results])

    for idx, vm in enumerate(vms):
        print(f"vm trace {idx}:")
        addrs = list(vm.execution_trace.keys())
        addrs.sort()
        for addr in addrs:
            print(f"{vm.execution_trace[addr]}")
        for ip in range(addrs[-1] + 1, len(vm.program)):
            print(f"{ip:5d}: {vm.program[ip]}")

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2019 - Day 7 - Amplification Circuit."
    )
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
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
