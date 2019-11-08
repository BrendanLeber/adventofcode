#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pdb
import sys
import traceback
from typing import Tuple

chars = "abcdefghijklmnopqrstuvwxyz"
bad_chars = ["i", "l", "o"]
couplets = None
triplets = None


def contains_triplet(password: str) -> bool:
    global chars, triplets
    if not triplets:
        triplets = []
        for start in range(0, len(chars) - 2):
            triplets.append(chars[start : start + 3])

    for triplet in triplets:
        if triplet in password:
            return True

    return False


def contains_bad_char(password: str) -> bool:
    global bad_chars
    for bc in bad_chars:
        if bc in password:
            return True
    return False


def contains_two_pairs(password: str) -> bool:
    global chars, couplets
    if not couplets:
        couplets = []
        for ch in chars:
            couplets.append(f"{ch}{ch}")

    found_one = False
    for couplet in couplets:
        if couplet in password:
            if found_one:
                return True
            else:
                found_one = True
    return False


def is_password_valid(password: str) -> bool:
    return (
        contains_triplet(password)
        and not contains_bad_char(password)
        and contains_two_pairs(password)
    )


def next_password(old: str) -> str:
    # break the password into a reversed list of digits
    digits = list(map(lambda ch: ord(ch) - ord("a"), old))
    digits.reverse()
    digits.append(-1)

    # increment the digits by one while handling the carry
    idx = 0
    while True:
        digits[idx] += 1
        if digits[idx] <= 25:
            break
        digits[idx] = 0
        idx += 1

    # assemble the digits back into a password
    if digits[-1] == -1:
        digits.pop()
    new = list(map(lambda digit: chr(ord("a") + digit), digits))
    new = "".join(reversed(new))

    return new


def solve(password: str) -> Tuple[int, int]:
    first = next_password(password)
    while not is_password_valid(first):
        first = next_password(first)

    second = next_password(first)
    while not is_password_valid(second):
        second = next_password(second)

    return (first, second)


if __name__ == "__main__":
    try:
        print(solve(sys.argv[1]))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
