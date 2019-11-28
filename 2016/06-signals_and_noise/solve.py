# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from typing import Dict, List, Tuple


def least_frequent(freqs: Dict[str, int]) -> str:
    skv = [(k, freqs[k]) for k in sorted(freqs, key=freqs.get)]
    return skv[0][0]


def most_frequent(freqs: Dict[str, int]) -> str:
    skv = [(k, freqs[k]) for k in sorted(freqs, key=freqs.get, reverse=True)]
    return skv[0][0]


def solve(messages: List[str], verbose=False) -> Tuple[str, str]:
    # create a list for each column of the messages that holds an empty dictionary
    pos_freqs: List[Dict[str, int]] = [None] * len(messages[0])  # type: ignore
    for pos in range(len(messages[0])):
        pos_freqs[pos] = {}

    # count the number of letters in each column of the messages
    for message in messages:
        for pos, ch in enumerate(message):
            pos_freqs[pos][ch] = pos_freqs[pos].get(ch, 0) + 1

    # part one is the most frequent character in each column
    # part two is the least frequent character in each column
    one_message: List[str] = []
    two_message: List[str] = []
    for pos in range(len(messages[0])):
        one_message.append(most_frequent(pos_freqs[pos]))
        two_message.append(least_frequent(pos_freqs[pos]))
    one: str = "".join(one_message)
    two: str = "".join(two_message)

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2016 - Day 6 - Signals and Noise."
    )
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Display extra info.  (Default: %(default)s)",
    )
    args = parser.parse_args()

    messages: List[str] = []
    with open(args.input) as inf:
        for line in inf:
            messages.append(line.strip())

    try:
        print(solve(messages, verbose=args.verbose))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
