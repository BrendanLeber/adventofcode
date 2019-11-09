#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fileinput
import json
import pdb
import traceback
from typing import Tuple

total = 0
no_reds = 0


def sum_ints(value) -> int:
    global total
    parsed = int(value)
    total += parsed
    return parsed


def total_without_reds(fragment):
    global no_reds

    if isinstance(fragment, list):
        for item in fragment:
            total_without_reds(item)
    elif isinstance(fragment, dict):
        if "red" not in fragment.values():
            for k, v in fragment.items():
                if isinstance(k, int):
                    no_reds += k
                total_without_reds(v)
    elif isinstance(fragment, int):
        no_reds += fragment
    elif isinstance(fragment, (str, float, True, False, None)):
        pass
    else:
        raise TypeError(f"{fragment} is of an unsupported type: {type(fragment)}")


def solve(doc: str) -> Tuple[int, int]:
    global total, no_reds

    total = 0
    objects = json.loads(doc, parse_int=sum_ints)

    no_reds = 0
    total_without_reds(objects)

    return (total, no_reds)


if __name__ == "__main__":
    try:
        for line in fileinput.input():
            line = line.strip()
            print(solve(line))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
