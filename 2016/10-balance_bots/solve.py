# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Tuple

Object_Type = Enum("Object_Type", ["UNKNOWN", "BOT", "OUTPUT"])


@dataclass
class Bot:
    low: int = -1
    high: int = -1


@dataclass
class Chip_Bot:
    chip: int = -1
    bot: int = -1


@dataclass
class Destination:
    object_type: Object_Type = Object_Type.UNKNOWN
    dest: int = -1


@dataclass
class Rule:
    low: Destination = Destination()
    high: Destination = Destination()


Inputs = List[Chip_Bot]
Rules = Dict[int, Rule]
Bots = Dict[int, Bot]
Output = List[int]
Outputs = Dict[int, Output]


VERBOSE: bool = False
bots: Bots = {}
inputs: Inputs = []
outputs: Outputs = {}
rules: Rules = {}
one: int = -1


def bot_give(bot_id: int, chip: int) -> None:
    if VERBOSE:
        print(f"giving chip {chip} to bot {bot_id}")

    bot = bots[bot_id]

    # give chip to this bot
    if bot.low == -1:
        bot.low = chip
    else:
        bot.high = chip
        if bot.high < bot.low:
            bot.high, bot.low = bot.low, bot.high

    # do we need to distribute more chips
    if (bot.low != -1) and (bot.high != -1):
        rule = rules[bot_id]

        if VERBOSE:
            ltype = "bot" if rule.low.object_type == Object_Type.BOT else "output"
            htype = "bot" if rule.high.object_type == Object_Type.BOT else "output"
            print(
                f"bot {bot_id} send chip {bot.low} to {ltype} {rule.low.dest} and chip {bot.high} to {htype} {rule.high.dest}"
            )

        # hard coded solution
        if bot.low == 17 and bot.high == 61:
            global one
            one = bot_id

        # hand off the lower chip
        if rule.low.object_type == Object_Type.BOT:
            bot_give(rule.low.dest, bot.low)
        else:
            output_give(rule.low.dest, bot.low)

        bot.low = -1

        # hand off the higher chip
        if rule.high.object_type == Object_Type.BOT:
            bot_give(rule.high.dest, bot.high)
        else:
            output_give(rule.high.dest, bot.high)

        bot.high = -1

    if VERBOSE:
        print(f"bot {bot_id} low {bot.low} high {bot.high}")


def initialize_bots() -> None:
    if VERBOSE:
        print("* initialize bots")

    for bot_id, rule in rules.items():
        if bot_id not in bots:
            bots[bot_id] = Bot()
            if VERBOSE:
                print(f"** {bot_id}: {bots[bot_id]}")

        low = rule.low
        if low.object_type == Object_Type.BOT:
            if low.dest not in bots:
                bots[low.dest] = Bot()
                if VERBOSE:
                    print(f"** {low.dest}: {bots[low.dest]}")

        high = rule.high
        if high.object_type == Object_Type.BOT:
            if high.dest in bots:
                bots[high.dest] = Bot()
                if VERBOSE:
                    print(f"** {high.dest}: {bots[high.dest]}")

    for inp in inputs:
        if inp.bot not in bots:
            bots[inp.bot] = Bot()
            if VERBOSE:
                print(f"** {inp.bot}: {bots[inp.bot]}")


def initialize_outputs() -> None:
    if VERBOSE:
        print("* initialize outputs")

    for rule in rules.values():
        low = rule.low
        if low.object_type == Object_Type.OUTPUT:
            if low.dest not in outputs:
                outputs[low.dest] = []
                if VERBOSE:
                    print(f"** {low.dest}: {outputs[low.dest]}")

        high = rule.high
        if high.object_type == Object_Type.OUTPUT:
            if high.dest not in outputs:
                outputs[high.dest] = []
                if VERBOSE:
                    print("f** {high.dest}: {outputs[high.dest]}")


def output_give(output: int, chip: int) -> None:
    if VERBOSE:
        print(f"giving chip {chip} to output {output}")
    outputs[output].append(chip)


def parse_commands(commands: List[Tuple[str, ...]]) -> None:
    if VERBOSE:
        print("* parse inputs & rules")

    for command in commands:
        if command[0] == "value":
            # value <chip> goes to bot <bot>
            inputs.append(Chip_Bot(int(command[1]), int(command[5])))
            if VERBOSE:
                print(f"** {inputs[-1]}")
        elif command[0] == "bot":
            # bot <bot> gives low to (output|bot) <low_id> and high to (output|bot) <high_id>
            bot_id: int = int(command[1])
            if bot_id in rules:
                raise ValueError(f"error inserting rule for bot {bot_id} which exists!")
            low_type = Object_Type.OUTPUT if command[5] == "output" else Object_Type.BOT
            low_id = int(command[6])
            high_type = Object_Type.OUTPUT if command[10] == "output" else Object_Type.BOT
            high_id = int(command[11])
            rule = Rule(Destination(low_type, low_id), Destination(high_type, high_id))
            rules[bot_id] = rule
            if VERBOSE:
                print(f"** {bot_id}: {rule}")
        else:
            raise ValueError(f"unknown command {command[0]}")


def solve(commands: List[Tuple[str, ...]]) -> Tuple[int, int]:
    parse_commands(commands)
    initialize_bots()
    initialize_outputs()

    if VERBOSE:
        print("* execute")
    for inp in inputs:
        if VERBOSE:
            print(f"give {inp.chip} to bot {inp.bot}")
        bot_give(inp.bot, inp.chip)

    # one: int = None
    two: int = outputs[0][0] * outputs[1][0] * outputs[2][0]

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2016 - Day 10 - Balance Bots.")
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
    VERBOSE = args.verbose

    commands: List[Tuple[str, ...]] = []
    with open(args.input) as inf:
        for line in inf:
            commands.append(tuple(line.strip().split()))
    try:
        print(solve(commands))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
