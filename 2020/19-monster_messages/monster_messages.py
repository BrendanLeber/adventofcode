# -*- coding: utf-8 -*-
"""Advent of Code 2020 - Day 19 - Monster Messages."""

import argparse
import pdb
import traceback


class Ref:
    def __init__(self, rules, index):
        self.rules = rules
        self.index = index

    def __getattr__(self, name):
        return getattr(self.rules[self.index], name)


class Rule:
    def accept(self, m):
        return any(len(m) == n for n in self.consume(m, 0))


class Char(Rule):
    @classmethod
    def parse(cls, rules, text):
        try:
            return Ref(rules, int(text))
        except ValueError:
            return cls(text[1])

    def __init__(self, ch):
        self.ch = ch

    def __repr__(self):
        return f"Char('{self.ch}')"

    def consume(self, m, i):
        if i < len(m) and m[i] == self.ch:
            yield 1


class Seq(Rule):
    @classmethod
    def parse(cls, rules, text):
        seq = text.split(" ")
        if 1 == len(seq):
            return Char.parse(rules, text)
        return cls([Char.parse(rules, w) for w in seq])

    @classmethod
    def _of(cls, rules):
        return cls(rules)

    def __init__(self, rules):
        self.rules = rules

    def consume(self, m, i):
        g = self.rules[0].consume(m, i)
        if 1 == len(self.rules):
            yield from g
        else:
            for n0 in g:
                for n1 in self._of(self.rules[1:]).consume(m, i + n0):
                    yield n0 + n1


class Or(Rule):
    @classmethod
    def parse(cls, rules, text):
        disjunction = text.split(" | ")
        if 1 == len(disjunction):
            return Seq.parse(rules, text)
        return cls([Seq.parse(rules, w) for w in disjunction])

    def __init__(self, rules):
        self.rules = rules

    def consume(self, m, i):
        for r in self.rules:
            yield from r.consume(m, i)


def parse_messages(data):
    messages = []
    for message in data.strip().split("\n"):
        messages.append(message)
    return messages


def parse_rules(data):
    rules = {}
    for line in data.split("\n"):
        rule_id, rest = line.strip().split(": ")
        rules[int(rule_id)] = Or.parse(rules, rest)
    return rules


def rules_matchp(rules, rid, value):
    rule = rules[rid]

    # match a single character
    if isinstance(rule, str):
        if value[0] == rule:
            return True, 1
        else:
            return False, 0

    # attempt to match every rule in the lists
    matches = []
    for submatch in rule:
        matches

    return False


def solve(text_rules, messages):
    rules = parse_rules(text_rules)
    one = 0
    for message in messages:
        if rules[0].accept(message):
            one += 1

    rules = parse_rules(text_rules + "\n8: 42 | 42 8\n11: 42 31 | 42 11 31")
    two = 0
    for message in messages:
        if rules[0].accept(message):
            two += 1

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2020 - Day 19 - Monster Messages."
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
            data = inf.read()
        sections = data.split("\n\n")
        messages = parse_messages(sections[1])
        print(solve(sections[0], messages))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
