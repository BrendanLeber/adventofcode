#!/usr/bin/env python
# -*- coding: utf-8 -*-

import fileinput
import pdb
import traceback


class Circuit:
    def __init__(self):
        self.gates = {}
        self.signals = {}

    def parse_segments(self, segments):
        for segment in segments:
            (instruction, wire) = segment.split(" -> ")
            instructions = instruction.split()
            if len(instructions) == 1:
                self.gates[wire] = intorvar(instructions[0])
            elif len(instructions) == 2:
                self.gates[wire] = (instructions[0].lower(), intorvar(instructions[1]))
            elif len(instructions) == 3:
                self.gates[wire] = (
                    instructions[1].lower(),
                    intorvar(instructions[0]),
                    intorvar(instructions[2]),
                )
            else:
                raise ValueError(f"'{segment}' is not valid.")

    def find(self, value):
        if value in self.signals:
            return self.signals[value]

        gate = self.gates[value]
        goal = self.execute(gate)
        self.signals[value] = goal
        return goal

    def execute(self, gate):
        if isinstance(gate, int):
            return gate
        elif isinstance(gate, str):
            return self.find(gate)

        if gate[0] == "not":
            op = gate[1]
            if op in self.signals:
                op = self.signals[op]
            else:
                op = self.find(op)
            return (~op) & 0xFFFF

        lhs = gate[1]
        if not isinstance(lhs, int):
            lhs = self.find(lhs)
        rhs = gate[2]
        if not isinstance(rhs, int):
            rhs = self.find(rhs)

        if gate[0] == "and":
            return (lhs & rhs) & 0xFFFF

        if gate[0] == "or":
            return (lhs | rhs) & 0xFFFF

        if gate[0] == "lshift":
            return (lhs << rhs) & 0xFFFF

        if gate[0] == "rshift":
            return (lhs >> rhs) & 0xFFFF

        raise ValueError(f"{gate[0]} is not a known gate!")


def intorvar(x):
    try:
        return int(x)
    except ValueError:
        return x


def solve(segments):
    circuit = Circuit()
    circuit.parse_segments(segments)

    a1 = circuit.find("a")
    circuit.signals = {}
    circuit.signals["b"] = a1

    a2 = circuit.find("a")

    return (a1, a2)


if __name__ == "__main__":
    try:
        segments = []
        for line in fileinput.input():
            segments.append(line.strip())
        print(solve(segments))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
