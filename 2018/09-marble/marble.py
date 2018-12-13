#!/usr/bin/env python


from dataclasses import dataclass
import fileinput


@dataclass
class Marble:
    value: int = 0
    left = None
    right = None


class CircularList:
    def __init__(self):
        self.head = Marble()
        self.head.left = self.head.right = self.head
        self.current = self.head

    def add(self, value):
        marble = Marble()
        marble.value = value

        after = self.current.right

        marble.left = after
        marble.right = after.right
        after.right.left = marble
        after.right = marble

        self.current = marble

    def remove(self):
        node = self.current
        for _ in range(7):
            node = node.left

        self.current = node.right

        node.left.right = node.right
        node.right.left = node.left
        node.left = None
        node.right = None

        return node.value

    def dump(self, player):
        print(f"[{player}] ", end="")
        node = self.head
        while True:
            if node == self.current:
                fragment = f"({node.value:d})"
            else:
                fragment = f" {node.value:d} "
            print(f"{fragment:5s}", end="")
            node = node.right
            if node == self.head:
                break
        print("")


def part_one(num_players, last_marble):
    scores = [0] * num_players
    player = 0

    marbles = CircularList()
    # marbles.dump("-")

    for marble in range(1, last_marble + 1):
        if marble % 23 == 0:
            scores[player] += marble
            scores[player] += marbles.remove()
        else:
            marbles.add(marble)

        # marbles.dump(player + 1)
        player = (player + 1) % num_players

    return max(scores)


if __name__ == "__main__":
    for line in fileinput.input():
        parts = line.strip().split()
        result = part_one(int(parts[0]), int(parts[6]))
        if len(parts) == 12:
            expected = int(parts[11])
            print(f"{result} {expected}")
        else:
            print(result)
