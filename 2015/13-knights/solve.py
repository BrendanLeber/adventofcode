#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fileinput
import pdb
import sys
import traceback
from itertools import permutations
from typing import List, Tuple


Seating = Tuple[str, int, str]


def decode_line(line: str) -> Seating:
    parts = line.strip().split()
    guest = parts[0]
    units = int(parts[3])
    neighbor = parts[10][:-1]
    if parts[2] == "lose":
        units = -units
    return (guest, units, neighbor)


def calculate_happiness(
    left: str, mid: str, right: str, seating: List[Seating]
) -> int:
    happiness = 0
    for seat in filter(lambda s: s[0] == mid, seating):
        if seat[2] == left or seat[2] == right:
            happiness += seat[1]

    return happiness


def total_happiness(guests: List[str], seating: List[Seating]) -> int:
    # first, last, & everyone in between
    happiness = calculate_happiness(guests[-1], guests[0], guests[1], seating)
    happiness += calculate_happiness(guests[-2], guests[-1], guests[0], seating)
    for idx in range(1, len(guests) - 1):
        happiness += calculate_happiness(guests[idx - 1], guests[idx], guests[idx + 1], seating)
    return happiness


def max_happiness(guests: List[str], seating: List[Seating]) -> int:
    max_happiness = -sys.maxsize
    for trie in permutations(guests):
        happiness = total_happiness(list(trie), seating)
        max_happiness = max(max_happiness, happiness)
    return max_happiness


def solve(seating: List[Seating]) -> Tuple[int, int]:
    guests = set()
    for lhs, _, rhs in seating:
        guests.add(lhs)
        guests.add(rhs)
    guest_list = list(guests)
    without_me = max_happiness(guest_list, seating)

    me = "*Brendan*"
    for guest in guest_list:
        seating.append((me, 0, guest))
        seating.append((guest, 0, me))
    guest_list.append(me)
    with_me = max_happiness(guest_list, seating)

    return (without_me, with_me)


if __name__ == "__main__":
    try:
        seating = []
        for line in fileinput.input():
            seating.append(decode_line(line))
        print(solve(seating))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
