#!/usr/bin/env python3
"""
Solve the Advent of Code Day 03 problem:
'Perfectly Spherical Houses in a Vacuum'.
"""

from __future__ import print_function
from collections import namedtuple

import fileinput
import sys


Position = namedtuple('Position', ['row', 'col'])


def eprint(*args, **kwargs):
    """Print to stderr."""
    print(*args, file=sys.stderr, *kwargs)


class Santa:
    """Simulate Santa's movements."""
    def __init__(self):
        self.row = 0
        self.col = 0

    def __repr__(self):
        return (f'{self.__class__.__name__}'
                f'(row={self.row!r}, col={self.col!r})')

    def __eq__(self, other):
        if other.__class__ is not self.__class__:
            return NotImplemented
        return (self.row, self.col) == (other.row, other.col)

    def move(self, order):
        """Move Santa based on the given order."""
        if order == '^':
            self.row -= 1
        elif order == 'v':
            self.row += 1
        elif order == '<':
            self.col -= 1
        elif order == '>':
            self.col += 1
        else:
            raise ValueError('invalid char {0} in input'.format(order))

    def position(self):
        """Return a Position tuple of Santa's current location."""
        return Position(row=self.row, col=self.col)


def solve_part_1(orders):
    """Solve part one of the puzzle."""

    santa = Santa()
    visited_houses = {}
    visited_houses[Position(row=0, col=0)] = 1

    for order in orders:
        # move santa based on the input order
        santa.move(order)
        pos = santa.position()

        # drop a present or update the number of presents at a house
        if pos in visited_houses:
            visited_houses[pos] += 1
        else:
            visited_houses[pos] = 1

    # how many houses had a present delivered?
    num_presents_delivered = len(visited_houses)

    return num_presents_delivered


def solve_part_2(orders):
    """Solve part two of the puzzle."""

    # starting positions for santa & robo_santa
    santa = Santa()
    robo_santa = Santa()

    # both santa & robo_santa visit the first house
    visited_houses = {}
    visited_houses[Position(row=0, col=0)] = 2

    while orders:
        # handle santa
        santa.move(orders.pop(0))
        santa_pos = santa.position()
        if santa_pos in visited_houses:
            visited_houses[santa_pos] += 1
        else:
            visited_houses[santa_pos] = 1

        # handle robo_santa
        robo_santa.move(orders.pop(0))
        robo_pos = robo_santa.position()
        if robo_pos in visited_houses:
            visited_houses[robo_pos] += 1
        else:
            visited_houses[robo_pos] = 1

    # how many houses had a present delivered?
    num_presents_delivered = len(visited_houses)

    return num_presents_delivered


def solve(data):
    """
    Solve the Advent of Code Day 03 Part 01 problem:
    'Perfectly Spherical Houses in a Vacuum'.
    """

    return (solve_part_1(data), solve_part_2(data))


if __name__ == '__main__':
    # read problem input from file or stdin
    puzzle_data = []
    for line in fileinput.input():
        puzzle_data.extend(list(line.strip()))

    print(solve(puzzle_data))
