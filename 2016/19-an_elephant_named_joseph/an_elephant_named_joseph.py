# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from typing import List, Tuple


def josephus(n: int, k: int) -> int:
    pos = 0
    for i in range(2, n + 1):
        pos = (pos + k) % i
    return pos + 1


class Node:
    def __init__(self, id: int) -> None:
        self.id = id
        self.next = None
        self.prev = None

    def delete(self) -> None:
        self.prev.next = self.next
        self.next.prev = self.prev


def gift_exchange(number_of_elves: int) -> int:
    elves = list(map(Node, range(number_of_elves)))
    for i in range(number_of_elves):
        elves[i].next = elves[(i + 1) % number_of_elves]
        elves[i].prev = elves[(i - 1) % number_of_elves]

    start = elves[0]
    mid = elves[number_of_elves // 2]

    for i in range(number_of_elves - 1):
        mid.delete()
        mid = mid.next
        if (number_of_elves - i) % 2 == 1:
            mid = mid.next
        start = start.next

    return start.id + 1


def solve(number_of_elves: int) -> Tuple[int, int]:
    one: int = josephus(number_of_elves, 2)
    two: int = gift_exchange(number_of_elves)
    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2016 - Day 19 - An Elephant Named Joseph."
    )
    parser.add_argument(
        "number_of_elves",
        type=int,
        default=3014387,
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    args = parser.parse_args()

    try:
        print(solve(args.number_of_elves))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
