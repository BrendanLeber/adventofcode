# -*- coding: utf-8 -*-

import fileinput
import pdb
import traceback
from dataclasses import dataclass
from typing import Iterator, List, Tuple


@dataclass
class Ingredient:
    name: str
    capacity: int
    durability: int
    flavor: int
    texture: int
    calories: int


def decode_ingredient(line: str) -> Ingredient:
    parts = line.strip().split()
    return Ingredient(
        parts[0][:-1],
        int(parts[2][:-1]),
        int(parts[4][:-1]),
        int(parts[6][:-1]),
        int(parts[8][:-1]),
        int(parts[10]),
    )


def calories(amounts: List[int], ingredients: List[Ingredient]) -> int:
    kcals = 0
    for amount, ingredient in zip(amounts, ingredients):
        kcals += ingredient.calories * amount
    return kcals


def score(amounts: List[int], ingredients: List[Ingredient]) -> int:
    capacity = durability = flavor = texture = 0
    for amount, ingredient in zip(amounts, ingredients):
        capacity += ingredient.capacity * amount
        durability += ingredient.durability * amount
        flavor += ingredient.flavor * amount
        texture += ingredient.texture * amount

    capacity = 0 if capacity < 0 else capacity
    durability = 0 if durability < 0 else durability
    flavor = 0 if flavor < 0 else flavor
    texture = 0 if texture < 0 else texture

    return capacity * durability * flavor * texture


def mixtures(n: int, total: int) -> Iterator[List[int]]:
    start = total if n == 1 else 0
    for i in range(start, total + 1):
        left = total - i
        if n - 1:
            for y in mixtures(n - 1, left):
                yield [i] + y
        else:
            yield [i]


def solve(ingredients: List[Ingredient]) -> Tuple[int, int]:
    score_full = score_500 = -1
    for amounts in mixtures(len(ingredients), 100):
        cookie_score = score(amounts, ingredients)
        score_full = max(score_full, cookie_score)

        kcals = calories(amounts, ingredients)
        if kcals == 500:
            score_500 = max(score_500, cookie_score)

    return (score_full, score_500)


if __name__ == "__main__":
    try:
        ingredients = []
        for line in fileinput.input():
            ingredients.append(decode_ingredient(line))
        print(solve(ingredients))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
