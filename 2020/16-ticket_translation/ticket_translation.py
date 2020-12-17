# -*- coding: utf-8 -*-
"""Advent of Code 2020 - Day 16 - Ticket Translation."""

import argparse
import pdb
import traceback
from collections import defaultdict
from math import prod
from re import findall, match


def count_valid_rules(rules, number):
    valid_rules = 0
    for rule, (lhs, rhs) in rules.items():
        if lhs[0] <= number <= lhs[1] or rhs[0] <= number <= rhs[1]:
            valid_rules += 1
    return valid_rules


def extract_ints(line):
    return [int(x) for x in findall(r"-?\d+", line)]


def parse_nearby(section):
    nearby = []
    lines = section.strip().split("\n")
    for line in lines[1:]:
        nearby.append(extract_ints(line.strip()))
    return nearby


def parse_rules(section):
    lines = section.strip().split("\n")
    rules = {}
    for line in lines:
        m = match(r"^([^:]+):\s+(\d+)-(\d+)\s+or\s+(\d+)-(\d+)$", line)
        rules[m[1]] = [
            (int(m[2]), int(m[3])),
            (int(m[4]), int(m[5])),
        ]
    return rules


def parse_ticket(section):
    lines = section.strip().split("\n")
    return extract_ints(lines[1].strip())


def solve(rules, my_ticket, nearby_tickets):
    valid_nearby_tickets = []
    invalid_numbers = []
    for ticket in nearby_tickets:
        all_valid = True
        for number in ticket:
            if count_valid_rules(rules, number) < 1:
                all_valid = False
                invalid_numbers.append(number)
        if all_valid:
            valid_nearby_tickets.append(ticket)
    one = sum(invalid_numbers)

    possible_rules = defaultdict(set)
    for idx, col in enumerate(zip(*valid_nearby_tickets)):
        for rule_name, (lhs, rhs) in rules.items():
            if all(lhs[0] <= j <= lhs[1] or rhs[0] <= j <= rhs[1] for j in col):
                possible_rules[rule_name].add(idx)

    field_columns = {}
    while possible_rules:
        solved_field = set()
        for field, cols in possible_rules.items():
            if len(cols) == 1:
                solved_field.add(field)
        solved_column = set()
        for field in solved_field:
            col = possible_rules.pop(field).pop()
            field_columns[field] = col
            solved_column.add(col)
        for col in solved_column:
            for cols in possible_rules.values():
                cols.discard(col)

    departure_numbers = []
    for field, column in field_columns.items():
        if field.startswith("departure"):
            departure_numbers.append(my_ticket[column])
    two = prod(departure_numbers)

    return (one, two)


def valid_ticket_number(rule, number):
    name, (lhs, rhs) = rule
    if lhs[0] <= number <= lhs[1] or rhs[0] <= number <= rhs[1]:
        return True
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2020 - Day 16 - Ticket Translation."
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
        with open(args.input, "rt") as inf:
            lines = inf.read()
        sections = lines.split("\n\n")
        rules = parse_rules(sections[0])
        ticket = parse_ticket(sections[1])
        nearby = parse_nearby(sections[2])

        print(solve(rules, ticket, nearby))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
