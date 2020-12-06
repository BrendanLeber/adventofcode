# -*- coding: utf-8 -*-
"""Advent of Code 2020 - Day 6 - Custom Customs."""

from __future__ import annotations

import argparse
import os
import pdb
import traceback
from typing import Dict, List, Set, Tuple


CharacterCounts = Dict[str, int]
Group = List[str]
Groups = List[Group]


def parse_input(fname: str) -> Groups:
    """Read the input file and return the parsed data."""
    with open(fname, "rt") as inf:
        raw: str = inf.read()
    blocks: List[str] = raw.split(2 * os.linesep)
    data: Groups = []
    for block in blocks:
        group: Group = []
        for person in block.split():
            group.append(person.strip())
        data.append(group)
    return data


def get_character_counts(string: str) -> CharacterCounts:
    chars: Set[str] = set(string)
    result: CharacterCounts = {}
    for ch in chars:
        result[ch] = string.count(ch)
    return result


def solve(groups: Groups) -> Tuple[int, int]:
    counts_per_group: List[int] = []
    for group in groups:
        answers_per_group: Set[str] = set("".join(group))
        group_count: int = len(answers_per_group)
        counts_per_group.append(group_count)
    one: int = sum(counts_per_group)

    counts_per_group = []
    for group in groups:
        group_count = 0
        cc: CharacterCounts = get_character_counts("".join(group))
        for (vote, votes) in cc.items():
            if votes == len(group):
                group_count += 1
        counts_per_group.append(group_count)
    two: int = sum(counts_per_group)
    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2020 - Day 6 - Custom Customs.")
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    args = parser.parse_args()

    try:
        data: Groups = parse_input(args.input)
        print(solve(data))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
