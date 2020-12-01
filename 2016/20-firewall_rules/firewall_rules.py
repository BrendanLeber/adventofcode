# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from typing import List, Tuple


def test_ip(ip: int, rules: List[Tuple[int, int]], max_addr: int) -> bool:
    for (start, end) in rules:
        if start <= ip <= end:
            break
    else:
        if ip < max_addr:
            return True
    return False


def solve(rules: List[Tuple[int, int]], max_addr: int) -> Tuple[int, int]:
    candidates = [rule[1] + 1 for rule in rules]
    valids = [candidate for candidate in candidates if test_ip(candidate, rules, max_addr)]
    one: int = valids[0]

    two: int = 0
    for ip in valids:
        while test_ip(ip, rules, max_addr):
            two += 1
            ip += 1

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2016 - Day 20 - Firewall Rules.")
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    parser.add_argument(
        "max_addr",
        type=int,
        default=4294967296,
        nargs="?",
        help="The largest address.  (Default %(default)s)",
    )
    args = parser.parse_args()

    rules: List[Tuple[int, int]] = []
    with open(args.input, "rt") as inf:
        for line in inf:
            parts = line.strip().split("-")
            rules.append((int(parts[0]), int(parts[1])))
    rules.sort()

    try:
        print(solve(rules, args.max_addr))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
