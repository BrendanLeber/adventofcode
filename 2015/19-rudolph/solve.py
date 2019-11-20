# -*- coding: utf-8 -*-

import argparse
import pdb
import re
import traceback
from typing import Dict, List, Set, Tuple

Replacement = Tuple[str, str]


def solve(replacements: List[Replacement], molecule: str) -> Tuple[int, int]:
    output: Set[str] = set()
    for src, dest in replacements:
        for pos in range(len(molecule)):
            if molecule.startswith(src, pos):
                out = molecule[:pos] + dest + molecule[pos + len(src):]
                output.add(out)

    dr: Dict[str, str] = {}
    for k, v in replacements:
        dr[v[::-1]] = k[::-1]

    def rep(x):
        return dr[x.group()]

    molecule = molecule[::-1]
    count: int = 0
    while molecule != "e":
        molecule = re.sub("|".join(dr.keys()), rep, molecule, count=1)
        count += 1

    return (len(output), count)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2015 - Day 19 - Medicine for Rudolph."
    )
    parser.add_argument("input", type=str, help="The puzzle input.")
    args = parser.parse_args()

    try:
        replacements: List[Replacement] = []
        with open(args.input) as inf:
            parse_replacements = True
            for line in inf:
                if parse_replacements and len(line) == 1:
                    parse_replacements = False
                    continue
                elif parse_replacements:
                    src, dest = line.split("=>")
                    replacements.append((src.strip(), dest.strip()))
                else:
                    molecule = line.strip()

        print(solve(replacements, molecule))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
