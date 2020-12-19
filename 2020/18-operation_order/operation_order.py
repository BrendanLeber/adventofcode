# -*- coding: utf-8 -*-
"""Advent of Code 2020 - Day 18 - Operation Order."""

import argparse
import operator
import pdb
import traceback
from copy import deepcopy


def evaluate(expression) -> int:
    operators = {"*": operator.mul, "+": operator.add}

    # handle sub-lists.
    for idx in range(len(expression)):
        if isinstance(expression[idx], list):
            expression[idx] = evaluate(expression[idx])

    # evaluate all terms, left to right.
    while len(expression) > 1:
        lhs, op, rhs = expression[0:3]
        expression = expression[3:]
        expression.insert(0, operators[op](lhs, rhs))

    return expression[0]


def evaluate2(expression) -> int:
    operators = {"*": operator.mul, "+": operator.add}

    # first handle sub-lists
    for idx, term in enumerate(expression):
        if isinstance(term, list):
            expression[idx] = evaluate2(term)

    # evaluate addition first.
    while "+" in expression:
        plus = expression.index("+")
        lhs, op, rhs = expression[plus - 1 : plus + 2]
        expression = expression[: plus - 1] + expression[plus + 2 :]
        if isinstance(lhs, list):
            lhs = evaluate2(lhs)
        if isinstance(rhs, list):
            rhs = evaluate2(rhs)
        expression.insert(plus - 1, operators[op](lhs, rhs))

    # evaluate remaining terms, left to right.
    while len(expression) > 1:
        lhs, op, rhs = expression[0:3]
        expression = expression[3:]
        expression.insert(0, operators[op](lhs, rhs))

    return expression[0]


def parse(expression):
    def _parse(it):
        terms = []
        for term in it:
            if term == "(":
                result = _parse(it)
                terms.append(result)
            elif term == ")":
                return terms
            elif term.isspace():
                continue
            elif term.isdigit():
                terms.append(int(term))
            elif term in ("+", "*"):
                terms.append(term)
        return terms

    return _parse(iter(expression))


def solve(expressions: list[str]):
    one_values = []
    two_values = []
    for expression in expressions:
        parsed = parse(expression)
        one_values.append(evaluate(deepcopy(parsed)))
        two_values.append(evaluate2(deepcopy(parsed)))
    one = sum(one_values)
    two = sum(two_values)
    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2020 - Day 18 - Operation Order."
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
        expressions: list[str] = []
        with open(args.input, "rt") as inf:
            expressions = inf.readlines()
        print(solve(expressions))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
