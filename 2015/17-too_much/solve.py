# -*- coding: utf-8 -*-

import argparse
import pdb
import sys
import traceback
from itertools import combinations
from typing import List, Tuple


def solve(target: int, containters: List[int]) -> Tuple[int, int]:
    one = 0
    solutions = []
    for bottles in range(len(containers)):
        for trie in combinations(containers, bottles):
            if sum(trie) == target:
                solutions.append(trie)
                one += 1

    min_bottles = sys.maxsize
    for solution in solutions:
        min_bottles = min(min_bottles, len(solution))

    two = 0
    for solution in solutions:
        if len(solution) == min_bottles:
            two += 1

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2015 - Day 17 - No Such Thing as Too Much."
    )
    parser.add_argument("input", type=str, help="The puzzle input.")
    parser.add_argument("target", type=int, default=150, nargs="?", help="The target value.")
    args = parser.parse_args()

    try:
        containers: List[int] = []
        with open(args.input) as inf:
            for line in inf:
                containers.append(int(line.strip()))
        print(solve(args.target, containers))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
