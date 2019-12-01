# -*- coding: utf-8 -*-

from __future__ import annotations

import argparse
import pdb
import traceback
from enum import Enum
from heapq import heappop, heappush
from typing import (Callable, Dict, Generic, List, NamedTuple, Optional, Tuple,
                    TypeVar)

T = TypeVar("T")


class Cell(str, Enum):
    EMPTY = "."
    BLOCKED = "#"
    START = "s"
    GOAL = "g"
    PATH = "O"


class Pos(NamedTuple):
    row: int
    column: int


class Node(Generic[T]):
    def __init__(self, state: T, parent: Optional[Node], cost: int = 0, heuristic: int = 0) -> None:
        self.state: T = state
        self.parent: Optional[Node] = parent
        self.cost: int = cost
        self.heuristic: int = heuristic

    def __lt__(self, other: Node) -> bool:
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)


VERBOSE: bool = False


class Maze:
    def __init__(
        self, width: int, height: int, number: int, goal: Pos, start: Pos = Pos(1, 1)
    ) -> None:
        self._width: int = width
        self._height: int = height
        self._number: int = number
        self.start: Pos = start
        self.goal: Pos = goal
        self._grid: List[List[Cell]] = [[Cell.EMPTY for _ in range(width)] for _ in range(height)]
        self._generate()
        self._grid[start.row][start.column] = Cell.START
        self._grid[goal.row][goal.column] = Cell.GOAL

    def __str__(self) -> str:
        output: str = ""
        for row in self._grid:
            output += "".join([c.value for c in row]) + "\n"
        return output

    def _generate(self) -> None:
        # add walls according to the problem description
        for y in range(self._height):
            for x in range(self._width):
                cell = x * x + 3 * x + 2 * x * y + y + y * y + self._number
                if bin(cell).count("1") & 1:
                    self._grid[y][x] = Cell.BLOCKED

    def goal_test(self, pos: Pos) -> bool:
        return pos == self.goal

    def successors(self, pos: Pos) -> List[Pos]:
        locations: List[Pos] = []
        if pos.row + 1 < self._height and self._grid[pos.row + 1][pos.column] != Cell.BLOCKED:
            locations.append(Pos(pos.row + 1, pos.column))
        if pos.row - 1 >= 0 and self._grid[pos.row - 1][pos.column] != Cell.BLOCKED:
            locations.append(Pos(pos.row - 1, pos.column))
        if pos.column + 1 < self._width and self._grid[pos.row][pos.column + 1] != Cell.BLOCKED:
            locations.append(Pos(pos.row, pos.column + 1))
        if pos.column - 1 >= 0 and self._grid[pos.row][pos.column - 1] != Cell.BLOCKED:
            locations.append(Pos(pos.row, pos.column - 1))
        return locations

    def mark(self, path: List[Pos]) -> None:
        for location in path:
            self._grid[location.row][location.column] = Cell.PATH

    def clear(self, path: List[Pos]) -> None:
        for location in path:
            self._grid[location.row][location.column] = Cell.EMPTY
        self._grid[self.start.row][self.start.column] = Cell.START
        self._grid[self.goal.row][self.goal.column] = Cell.GOAL


class PriorityQueue(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    def __repr__(self) -> str:
        return repr(self._container)

    def empty(self) -> bool:
        return not self._container

    def pop(self) -> T:
        return heappop(self._container)

    def push(self, item: T) -> None:
        heappush(self._container, item)


def astar(
    initial: T,
    goal_test: Callable[[T], bool],
    successors: Callable[[T], List[T]],
    heuristic: Callable[[T], int],
) -> Optional[Node[T]]:
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(initial, None, 0, heuristic(initial)))
    explored: Dict[T, int] = {initial: 0}
    while not frontier.empty():
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        if goal_test(current_state):
            return current_node
        for child in successors(current_state):
            new_cost: int = current_node.cost + 1
            if child not in explored or explored[child] > new_cost:
                explored[child] = new_cost
                frontier.push(Node(child, current_node, new_cost, heuristic(child)))
    return None


def astar2(
    initial: T,
    goal_test: Callable[[T], bool],
    successors: Callable[[T], List[T]],
    heuristic: Callable[[T], int],
    steps: int,
) -> int:
    frontier: PriorityQueue[Node[T]] = PriorityQueue()
    frontier.push(Node(initial, None, 0, heuristic(initial)))
    explored: Dict[T, int] = {initial: 0}
    while not frontier.empty():
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        # if goal_test(current_state):
        #    return current_node
        for child in successors(current_state):
            new_cost: int = current_node.cost + 1
            if child not in explored or explored[child] > new_cost:
                explored[child] = new_cost
                frontier.push(Node(child, current_node, new_cost, heuristic(child)))
    steps_or_less = [kv for kv in explored.items() if kv[1] <= steps]
    return len(steps_or_less)


def node_to_path(node: Node[T]) -> List[T]:
    path: List[T] = [node.state]
    while node.parent is not None:
        node = node.parent
        path.append(node.state)
    path.reverse()
    return path


def manhattan_distance(goal: Pos) -> Callable[[Pos], int]:
    def distance(pos: Pos) -> int:
        xdist: int = abs(goal.column - pos.column)
        ydist: int = abs(goal.row - pos.row)
        return xdist + ydist

    return distance


def solve(designer_number: int, goal: Pos) -> Tuple[int, int]:
    start: Pos = Pos(1, 1)
    maze = Maze(50, 50, designer_number, goal, start)
    if VERBOSE:
        print(f"number: {designer_number}  {start} -> {goal}")
        print(maze)

    distance: Callable[[Pos], int] = manhattan_distance(maze.goal)
    solution: Optional[Node[Pos]] = astar(maze.start, maze.goal_test, maze.successors, distance)
    if solution is None:
        raise ValueError("No solution found!")
    path: List[Pos] = node_to_path(solution)
    if VERBOSE:
        maze.mark(path)
        print(f"Solution length: {len(path) - 1}\n{maze}")
        maze.clear(path)

    one: int = len(path) - 1
    two: int = astar2(maze.start, maze.goal_test, maze.successors, distance, 50)

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2016 - Day 13 - A Maze of Twisty Little Cubicles."
    )
    parser.add_argument(
        "input", type=int, default=1352, nargs="?", help="The puzzle input.  (Default %(default)s)"
    )
    parser.add_argument(
        "destination",
        type=str,
        default="31,39",
        nargs="?",
        help="The destination (col,row) square.  (Default %(default)s)",
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        default=False,
        help="Display extra info.  (Default: %(default)s)",
    )
    args = parser.parse_args()
    VERBOSE = args.verbose

    try:
        target = tuple(map(int, args.destination.split(",")))
        print(solve(args.input, Pos(column=target[0], row=target[1])))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
