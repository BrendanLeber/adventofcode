#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pdb
import sys
import traceback
from typing import Tuple


def look_and_say(sequence: str) -> str:
    # create a run-length list of (char, count) from the input
    rle = []
    old_ch = sequence[0]
    counter = 1
    for ch in sequence[1:]:
        if old_ch != ch:
            rle.append((old_ch, counter))
            old_ch = ch
            counter = 1
        else:
            counter += 1
    rle.append((old_ch, counter))

    # build the new say sequence from the character counts
    result = []
    for ch, count in rle:
        result.append(str(count))
        result.append(ch)

    # reassemble into a string as required by the specification
    result = "".join(result)

    return result


def solve(number: str) -> Tuple[int, int]:
    part_1 = number
    for _ in range(40):
        part_1 = look_and_say(part_1)

    part_2 = part_1
    for _ in range(10):
        part_2 = look_and_say(part_2)

    return (len(part_1), len(part_2))


if __name__ == "__main__":
    try:
        print(solve(sys.argv[1]))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
