# -*- coding: utf-8 -*-
"""Advent of Code 2020 - Day 7 - Handy Haversacks."""

import argparse
import pdb
import traceback

RULES = {}


def parse_input(fname: str):
    """Read the input file and return the parsed data."""
    data = {}
    with open(fname, "rt") as inf:
        for line in inf:
            (bag_type, contents) = line.split(" contain ")
            bag_type = " ".join(bag_type.split(" ")[0:2])
            data[bag_type] = []
            bags = contents.split(",")
            for bag in bags:
                parts = bag.split()
                if parts[0] != "no":
                    num = int(parts[0])
                    color = " ".join(parts[1:3])
                    data[bag_type].append((num, color))
    return data


def can_contain(root, goal):
    result = 0
    for _, rule in RULES[root]:
        if rule == goal:
            result += 1
        result += can_contain(rule, goal)
    return result


def count_bags(root):
    result = 0
    for num, rule in RULES[root]:
        result += num + num * count_bags(rule)
    return result


def solve(goal_bag):
    one = 0
    for bag in RULES:
        if bag == goal_bag:
            continue  # skip because we can't contain ourself
        if can_contain(bag, goal_bag) > 0:
            one += 1

    two = count_bags(goal_bag)
    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2020 - Day 7 - Handy Haversacks."
    )
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    parser.add_argument(
        "--goal",
        type=str,
        default="shiny gold",
        help="The goal bag.  (Default %(default)s)",
    )
    args = parser.parse_args()

    try:
        RULES = parse_input(args.input)
        print(solve(args.goal))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
