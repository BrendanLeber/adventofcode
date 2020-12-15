# -*- coding: utf-8 -*-
"""Advent of Code 2020 - Day 13 - Shuttle Search."""

import argparse
import pdb
import traceback


def solve(start, busses):
    now = start
    stop = 0
    here = 0
    while not here:
        for bus_id in busses:
            if bus_id != "x" and not now % bus_id:
                here = bus_id
                stop = now
                break
        now += 1
    one = (stop - start) * here

    buss_offsets = [(bus, idx) for idx, bus in enumerate(busses) if bus != "x"]
    now, step = 0, 1
    for bid, offset in buss_offsets:
        while (now + offset) % bid != 0:
            now += step
        step *= bid

    two = now
    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2020 - Day 13 - Shuttle Search.")
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    args = parser.parse_args()

    try:
        timestamp: int = 0
        busses = []
        with open(args.input, "rt") as inf:
            lines = inf.readlines()
            timestamp = int(lines[0])
            for bus_id in lines[1].strip().split(","):
                if bus_id != "x":
                    busses.append(int(bus_id))
                else:
                    busses.append(bus_id)

        print(solve(timestamp, busses))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
