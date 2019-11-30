# -*- coding: utf-8 -*-

from heapq import heappop, heappush
from itertools import combinations


# hardcoded input
promethium, cobalt, curium, ruthenium, plutonium, elerium, dilithium = 1, 2, 3, 4, 5, 6, 7
initial = (
    0,
    (
        tuple(sorted((promethium, -promethium, elerium, -elerium, dilithium, -dilithium))),
        tuple(sorted((cobalt, curium, ruthenium, plutonium))),
        tuple(sorted((-cobalt, -curium, -ruthenium, -plutonium))),
        (),
    ),
)


def correct(floor):
    if not floor or floor[-1] < 0:  # no generators
        return True
    return all(-chip in floor for chip in floor if chip < 0)


frontier = []
heappush(frontier, (0, initial))
cost_so_far = {initial: 0}

while frontier:
    _, current = heappop(frontier)
    floor, floors = current
    if floor == 3 and all(len(f) == 0 for f in floors[:-1]):  # goal!
        break

    directions = [dir for dir in (-1, 1) if 0 <= floor + dir < 4]
    moves = list(combinations(floors[floor], 2)) + list(combinations(floors[floor], 1))
    for move in moves:
        for direction in directions:
            new_floors = list(floors)
            new_floors[floor] = tuple(x for x in floors[floor] if x not in move)
            new_floors[floor + direction] = tuple(sorted(floors[floor + direction] + move))

            if not correct(new_floors[floor]) or not correct(new_floors[floor + direction]):
                continue

            next_state = (floor + direction, tuple(new_floors))
            new_cost = cost_so_far[current] + 1
            if next_state not in cost_so_far or new_cost < cost_so_far[next_state]:
                cost_so_far[next_state] = new_cost
                priority = new_cost - len(new_floors[3]) * 10  # silly manual tweakable heuristic
                heappush(frontier, (priority, next_state))


print(cost_so_far[current], current)
