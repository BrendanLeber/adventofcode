# -*- coding: utf-8 -*-

import fileinput
import pdb
import traceback
from typing import Dict, List, Tuple

Aunts = Dict[int, Dict[str, int]]


def solve(aunts: Aunts) -> Tuple[int, int]:
    ticker_tape: Dict[str, int] = {
        "children": 3,
        "cats": 7,
        "samoyeds": 2,
        "pomeranians": 3,
        "akitas": 0,
        "vizslas": 0,
        "goldfish": 5,
        "trees": 3,
        "cars": 2,
        "perfumes": 1,
    }

    one: List[int] = []
    two: List[int] = []
    for n, aunt in aunts.items():
        if all(ticker_tape[k] == v for k, v in aunt.items()):
            one.append(n)

        for k, v in aunt.items():
            if k in ["cats", "trees"]:
                if v < ticker_tape[k]:
                    break
            elif k in ["pomeranians", "goldfish"]:
                if v > ticker_tape[k]:
                    break
            else:
                if v != ticker_tape[k]:
                    break
        else:
            two.append(n)

    two = [n for n in two if n not in one]

    return (one[0], two[0])


if __name__ == "__main__":
    try:
        aunts: Aunts = {}
        for line in fileinput.input():
            _, n, a, an, b, bn, c, cn = line.strip().replace(",", "").replace(":", "").split()
            aunts[int(n)] = {a: int(an), b: int(bn), c: int(cn)}
        print(solve(aunts))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
