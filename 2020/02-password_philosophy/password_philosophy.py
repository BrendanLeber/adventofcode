# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from typing import List, Tuple

Policy = Tuple[int, int]  # lowest, highest number of times character can appear
Letter = str
Password = str
Entry = Tuple[Policy, Letter, Password]
Database = List[Entry]


def parse_input(fname: str) -> Database:
    """Read the input file and return the parsed data."""
    db: Database = []
    with open(args.input, "rt") as inf:
        for line in inf:
            parts = line.strip().split()
            policy = parts[0].split("-")
            entry: Entry = ((int(policy[0]), int(policy[1])), parts[1][0], parts[2])
            db.append(entry)
    return db


def count_valid_entries(db: Database) -> Tuple[int, int]:
    """Count the number of valid passwords according to the policies."""
    one: int = 0
    two: int = 0
    for (policy, letter, password) in db:
        # part one, min and max number of occurrences
        num_letters: int = password.count(letter)
        if policy[0] <= num_letters <= policy[1]:
            one += 1
        # part two, either or but not both is a match
        num_valid: int = 0
        if password[policy[0] - 1] == letter:
            num_valid += 1
        if password[policy[1] - 1] == letter:
            num_valid += 1
        if num_valid == 1:
            two += 1
    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2020 - Day 2 - Password Philosophy."
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
        db: Database = parse_input(args.input)
        print(count_valid_entries(db))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
