# -*- coding: utf-8 -*-

import argparse
import pdb
import sys
import traceback
from collections import namedtuple
from dataclasses import dataclass
from itertools import combinations
from typing import List, Tuple


@dataclass
class Character:
    hp: int
    damage: int
    armor: int


Item = namedtuple("Item", ["name", "cost", "damage", "armor"])


def simulate_round(attacker: Character, defender: Character) -> bool:
    ahp = attacker.hp
    dhp = defender.hp
    while True:
        dmg = max(attacker.damage - defender.armor, 1)
        dhp -= dmg
        if dhp <= 0:
            return True

        dmg = max(defender.damage - attacker.armor, 1)
        ahp -= dmg
        if ahp <= 0:
            return False


def solve(player: Character, boss: Character) -> Tuple[int, int]:
    weapons: List[Item] = [
        Item("Dagger", 8, 4, 0),
        Item("Shortsword", 10, 5, 0),
        Item("Warhammer", 25, 6, 0),
        Item("Longsword", 40, 7, 0),
    ]

    armors: List[Item] = [
        Item("Leather", 13, 0, 1),
        Item("Chainmail", 31, 0, 2),
        Item("Splintmail", 53, 0, 3),
        Item("Bandedmail", 75, 0, 4),
        Item("Platemail", 102, 0, 5),
        Item("None", 0, 0, 0),
    ]

    rings: List[Item] = [
        Item("Damage +1", 25, 1, 0),
        Item("Damage +2", 50, 2, 0),
        Item("Damage +3", 100, 3, 0),
        Item("Defense +1", 20, 0, 1),
        Item("Defense +2", 40, 0, 2),
        Item("Defense +3", 80, 0, 3),
        Item("None A", 0, 0, 0),
        Item("None B", 0, 0, 0),
    ]

    one = sys.maxsize
    two = -sys.maxsize
    for weapon in weapons:
        for armor in armors:
            for left, right in combinations(rings, 2):
                cost = weapon.cost + armor.cost + left.cost + right.cost
                player.damage = weapon.damage + armor.damage + left.damage + right.damage
                player.armor = weapon.armor + armor.armor + left.armor + right.armor
                if simulate_round(player, boss):
                    one = min(one, cost)
                else:
                    two = max(two, cost)

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2015 - Day 21 - RPG Simulator 20XX."
    )
    # parser.add_argument("input", type=str, help="The puzzle input.")
    args = parser.parse_args()

    try:
        boss = Character(100, 8, 2)
        player = Character(100, 0, 0)
        print(solve(player, boss))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
