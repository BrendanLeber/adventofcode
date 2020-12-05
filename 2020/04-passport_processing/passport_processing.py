# -*- coding: utf-8 -*-
"""Advent of Code 2020 - Day 4 - Passport Processing."""

from __future__ import annotations

import argparse
import os
import pdb
import re
import traceback
from typing import Dict, List


REQUIRED_KEYS = {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"}
OPTIONAL_KEYS = {"cid"}
VALID_EYE_COLORS = {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}


def parse_input(fname: str) -> List[Dict[str, str]]:
    """Read the input file and return the parsed data."""
    with open(fname, "rt") as inf:
        raw: str = inf.read()
    blocks: List[str] = raw.split(2 * os.linesep)
    data: List[Dict[str, str]] = []
    for block in blocks:
        passport: Dict[str, str] = {}
        for segment in block.replace("\n", " ").split():
            (key, value) = segment.split(":")
            passport[key] = value
        data.append(passport)
    return data


def has_all_required_keys(passport: Dict[str, str]) -> bool:
    """Return true if the given passport contains all of the required keys."""
    for required in REQUIRED_KEYS:
        if required not in passport.keys():
            return False
    return True


def one(passports: List[Dict[str, str]]) -> int:
    valid: int = 0
    for passport in passports:
        if has_all_required_keys(passport):
            valid += 1
    return valid


def two(passports: List[Dict[str, str]]) -> int:
    hcl_re = re.compile("^#[0-9a-f]{6}$")
    pid_re = re.compile("^[0-9]{9}$")
    valid: int = 0
    for passport in passports:
        if not has_all_required_keys(passport):
            continue

        if not "1920" <= passport["byr"] <= "2002":
            continue

        if not "2010" <= passport["iyr"] <= "2020":
            continue

        if not "2020" <= passport["eyr"] <= "2030":
            continue

        if passport["hgt"][-2:] not in ("cm", "in"):
            continue
        if passport["hgt"][-2:] == "cm":
            if not "150" <= passport["hgt"][:-2] <= "193":
                continue
        else:
            if not "59" <= passport["hgt"][:-2] <= "76":
                continue

        if not hcl_re.match(passport["hcl"]):
            continue

        if passport["ecl"] not in VALID_EYE_COLORS:
            continue

        if not pid_re.match(passport["pid"]):
            continue

        valid += 1
    return valid


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2020 - Day 4 - Passport Processing."
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
        passports: Dict[str, str] = parse_input(args.input)
        print(one(passports))
        print(two(passports))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
