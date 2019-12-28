# -*- coding: utf-8 -*-

import argparse
import math
import pdb
import traceback
from typing import List


def get_pattern(phase: int, size: int) -> List[int]:
    BASE_PATTERN = [0, 1, 0, -1]
    result: List[int] = []
    while len(result) < size + 1:
        for pattern in BASE_PATTERN:
            result.extend([pattern] * phase)
    return result[1 : size + 1]


def get_message_1(signal: List[int], num_phases: int) -> str:
    MESSAGE_SIZE = 8
    one = signal[:]
    for _ in range(num_phases):
        one = phase(one)
    return "".join(map(str, one[:MESSAGE_SIZE]))


def get_message_2(signal: List[int], num_phases: int) -> str:
    OFFSET_SIZE = 7
    MULTIPLIER = 10000
    MESSAGE_SIZE = 8

    message_offset = int("".join(map(str, signal[:OFFSET_SIZE])))
    data_length = len(signal) * MULTIPLIER
    assert message_offset > data_length / 2
    necessary_length = data_length - message_offset
    num_copies = math.ceil(necessary_length / len(signal))
    input_data = signal[:] * num_copies
    input_data = input_data[-necessary_length:]

    output = input_data[:]
    for _ in range(num_phases):
        total = 0
        for j in range(len(output) - 1, -1, -1):
            total += output[j]
            output[j] = total % 10

    return "".join(map(str, output[:MESSAGE_SIZE]))


def phase(signal: List[int]) -> List[int]:
    end = []
    for cycle in range(1, len(signal) + 1):
        pattern = get_pattern(cycle, len(signal))
        total = 0
        for p, s in zip(pattern, signal):
            total += s * p
        end.append(abs(total) % 10)
    return end


def solve(signal: List[int]):
    one = get_message_1(signal, 100)
    two = get_message_2(signal, 100)
    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2019 - Day 16 - Flawed Frequency Transmission."
    )
    parser.add_argument("input", type=str, help="The puzzle input.")
    args = parser.parse_args()

    try:
        signal = list(map(int, list(args.input)))
        print(solve(signal))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
