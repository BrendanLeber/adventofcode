#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fileinput
import pdb
import sys
import traceback
from itertools import permutations


def solve(paths):
    cities = set()
    distances = dict()
    for start, end, distance in paths:
        cities.add(start)
        cities.add(end)
        distances.setdefault(start, dict())[end] = distance
        distances.setdefault(end, dict())[start] = distance

    shortest = sys.maxsize
    longest = -sys.maxsize
    for items in permutations(cities):
        dist = sum(map(lambda x, y: distances[x][y], items[:-1], items[1:]))
        shortest = min(shortest, dist)
        longest = max(longest, dist)

    return (shortest, longest)


if __name__ == "__main__":
    try:
        lines = []
        for line in fileinput.input():
            parts = line.strip().split()
            lines.append((parts[0], parts[2], int(parts[4])))
        print(solve(lines))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
