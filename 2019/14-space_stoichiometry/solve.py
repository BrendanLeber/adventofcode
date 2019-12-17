# -*- coding: utf-8 -*-

import argparse
import math
import pdb
import traceback


def extract_chemical(line):
    # ## XXXX -> (str, int)
    num, name = line.strip().split()
    if name[-1] == ",":
        name = name[:-1]
    return (name, int(num))


def extract_reaction(line: str):
    # ## AA[, ## BB...] => ## OO -> ((str, int), [(str, int),...])
    ins, out = line.split(" => ")
    output = extract_chemical(out)
    inputs = []
    for part in ins.split(","):
        inputs.append(extract_chemical(part))
    return (output, inputs)


def fibonacci(n, f0=0, f1=1):
    """Calculate the Nth Fibonacci Number."""
    for _ in range(n):
        f0, f1 = f1, f0 + f1
    return f0


def solve(reactions, trace):
    if trace:
        print("*** reactions:")
        for chemical in reactions.keys():
            print(f"{chemical} <= {reactions[chemical]}")

    # undo the reactions to find the amount of ORE we need
    one = undo_reactions({"FUEL": 1}, reactions, trace)
    if trace:
        print(f"1 FUEL requires {one} ORE to produce.")

    # use fibonacci sequence to quickly find a range containing the answer
    target = 1000000000000
    n = 2
    ores = -1
    low, high = -1, -1
    while ores < target:
        n += 1
        low, high = high, fibonacci(n)
        ores = undo_reactions({"FUEL": high}, reactions, trace)
        if trace:
            print(f"{low} {high} {n} {ores}")

    # use a binary search to narrow the range to the right value
    if trace:
        print(f"low {low}  high {high}")
    two = None
    while low <= high:
        mid = (low + high) // 2
        ores = undo_reactions({"FUEL": mid}, reactions, trace)
        if trace:
            print(f"{low} {mid} {high} {ores}")
        if ores < target:
            low = mid + 1
        elif ores > target:
            high = mid - 1
        else:
            two = mid
            break

    # we didn't find an exact answer so back down until we are under our target
    if not two:
        two = mid
        while undo_reactions({"FUEL": two}, reactions, trace) > target:
            two -= 1

    return (one, two)


def undo_reactions(target, reactions, trace):
    produced = target
    while True:
        eligible = [
            material for material in produced.keys() if produced[material] > 0 and material != "ORE"
        ]
        if not eligible:
            return produced["ORE"]

        have_mat = eligible[0]
        have_qty = produced[have_mat]

        run_count = math.ceil(have_qty / reactions[have_mat]["quantity"])

        for input_mat, input_qty in reactions[have_mat].items():
            if input_mat == "quantity":
                continue
            produced[input_mat] = produced.get(input_mat, 0) + input_qty * run_count
        produced[have_mat] -= reactions[have_mat]["quantity"] * run_count

    return None


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2019 - Day 14 - Space Stoichiometry."
    )
    parser.add_argument("input", type=str, help="The puzzle input")
    parser.add_argument(
        "--trace", action="store_true", default=False, help="Display a trace of execution."
    )
    args = parser.parse_args()

    reactions = {}
    with open(args.input) as inf:
        for line in inf:
            output, inputs = extract_reaction(line.strip())
            reactions[output[0]] = {"quantity": output[1]}
            reactions[output[0]].update(dict(inputs))

    try:
        print(solve(reactions, args.trace))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
