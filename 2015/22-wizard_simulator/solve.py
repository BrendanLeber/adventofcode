# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from collections import namedtuple
from functools import reduce
from heapq import heappop, heappush
from itertools import count
from typing import Tuple


class Spell(
    namedtuple("BaseSpell", ["name", "cost", "effect", "turns", "damage", "heal", "armor", "mana"])
):
    def __new__(cls, name, cost, effect=False, turns=None, damage=0, heal=0, armor=0, mana=0):
        return super().__new__(cls, name, cost, effect, turns, damage, heal, armor, mana)


spells = (
    Spell("Magic Missile", 53, damage=4),
    Spell("Drain", 73, damage=2, heal=2),
    Spell("Shield", 113, effect=True, turns=6, armor=7),
    Spell("Poison", 173, effect=True, turns=6, damage=3),
    Spell("Recharge", 229, effect=True, turns=5, mana=101),
)


class State:
    def __init__(
        self,
        hp,
        mana,
        boss_hp,
        boss_damage,
        mana_spent=0,
        effects=None,
        hard=False,
        parent=None,
        spell_cast=None,
    ):
        self.hp = hp
        self.mana = mana
        self.boss_hp = boss_hp
        self.boss_damage = boss_damage
        self.mana_spent = mana_spent
        self.effects = effects or ()
        self.hard = hard
        self._parent = parent
        self._spell_cast = spell_cast

    def __repr__(self) -> str:
        return f"State(hp={self.hp}, m={self.mana}, bhp={self.boss_hp}, bdmg={self.boss_damage}, ms={self.mana_spent}, effects={self.effects}, sp={self._spell_cast})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, State):
            return NotImplemented
        return all(getattr(self, k) == getattr(other, k) for k in vars(self) if k[0] != "_")

    def __hash__(self):
        return reduce(
            lambda a, b: a ^ hash(b), (v for k, v in vars(self).items() if k[0] != "_"), 0
        )

    def iter_path(self):
        if self._parent is None:
            return
        yield from self._parent.iter_path()
        yield self._spell_cast

    def process_effects(self, effects, hp, mana, boss_hp):
        remaining_effects = []
        armor = 0
        for timer, effect in self.effects:
            hp += effect.heal
            mana += effect.mana
            boss_hp -= effect.damage
            armor = max(armor, effect.armor)
            if timer > 1:
                remaining_effects.append((timer - 1, effect))
        return tuple(remaining_effects), hp, mana, boss_hp, armor

    def boss_turn(self):
        self.effects, self.hp, self.mana, self.boss_hp, armor = self.process_effects(
            self.effects, self.hp, self.mana, self.boss_hp
        )
        if self.boss_hp > 0:
            self.hp -= max(1, self.boss_damage - armor)

    def transitions(self):
        # player turn first
        effects, hp, mana, boss_hp, _ = self.process_effects(
            self.effects, self.hp - int(self.hard), self.mana, self.boss_hp
        )
        for spell in spells:
            if spell.cost > mana or any(spell is s for t, s in effects):
                continue
            new_state = State(
                hp,
                mana - spell.cost,
                boss_hp,
                self.boss_damage,
                self.mana_spent + spell.cost,
                effects,
                hard=self.hard,
                parent=self,
                spell_cast=spell.name,
            )
            if not spell.effect:
                new_state.hp += spell.heal
                new_state.boss_hp -= spell.damage
            else:
                new_state.effects = new_state.effects + ((spell.turns, spell),)

            new_state.boss_turn()
            if new_state.hp > 0:
                yield new_state


def search_a_star(start):
    open_states = {start}
    pqueue = [(0, start)]
    closed_states = set()
    unique = count()
    while open_states:
        current = heappop(pqueue)[-1]
        if current.boss_hp < 1:
            return current
        open_states.remove(current)
        closed_states.add(current)
        for state in current.transitions():
            if state in closed_states or state in open_states:
                continue
            open_states.add(state)
            heappush(pqueue, (state.mana_spent, next(unique), state))


def solve(player_hp, player_mana, boss_hp, boss_damage, verbose=False) -> Tuple[int, int]:
    one = None
    start = State(player_hp, player_mana, boss_hp, boss_damage)
    end = search_a_star(start)
    one = end.mana_spent
    if verbose:
        print("One: ", sep="")
        print(*end.iter_path(), sep=" -> ")

    two = None
    start = State(player_hp, player_mana, boss_hp, boss_damage, hard=True)
    end = search_a_star(start)
    two = end.mana_spent
    if verbose:
        print("Two: ", sep="")
        print(*end.iter_path(), sep=" -> ")

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2015 - Day 22 - Wizard Simulator 20XX."
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

    player_hp = 50
    player_mana = 500

    with open(args.input) as inf:
        boss_hp = int(next(inf).rpartition(":")[-1])
        boss_damage = int(next(inf).rpartition(":")[-1])

    try:
        print(solve(player_hp, player_mana, boss_hp, boss_damage, verbose=args.verbose))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
