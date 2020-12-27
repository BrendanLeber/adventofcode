# -*- coding: utf-8 -*-
"""Advent of Code 2020 - Day 22 - Crab Combat."""

import argparse
import pdb
import traceback


class Game:
    def __init__(self):
        self.round: int = 0
        self.decks: list[list[int], list[int]] = []
        self.picks: list[int] = []

    @classmethod
    def parse_puzzle(cls, puzzle: str):
        game: Game = cls()
        for section in puzzle.strip().split("\n\n"):
            deck = []
            cards = list(section.strip().split("\n"))[1:]
            for card in cards:
                deck.append(int(card))
            game.decks.append(deck)
        return game

    def _print_picks(self) -> None:
        print(f"Player 1 plays: {self.picks[0]}")
        print(f"Player 2 plays: {self.picks[1]}")

    def _print_post_game(self) -> None:
        print("\n== Post-game results ==")
        for player, deck in enumerate(self.decks):
            pdeck = ", ".join(map(str, deck))
            if len(pdeck):
                pdeck = " " + pdeck
            print(f"Player {player+1}'s deck:{pdeck}")

    def _print_start(self) -> None:
        print(f"-- Round {self.round} --")

        for player, deck in enumerate(self.decks):
            pdeck = ", ".join(map(str, deck))
            if len(pdeck):
                pdeck = " " + pdeck
            print(f"Player {player+1}'s deck:{pdeck}")

    def _print_winner(self) -> None:
        print(f"Player {self.winner+1} wins the round!")

    def game_over(self) -> bool:
        if any(not len(deck) for deck in self.decks):
            return True
        return False

    def get_score(self) -> tuple[int, int]:
        score: int = 0
        for idx, card in enumerate(reversed(self.decks[self.winner])):
            score += card * (idx + 1)
        return (self.winner + 1, score)

    def play_game(self, verbose: bool = False) -> tuple[int, int]:
        while not game.game_over():
            game.take_turn(verbose)
        if verbose:
            game._print_post_game()
        return game.get_score()

    def take_turn(self, verbose: bool = False) -> None:
        self.round += 1
        if verbose:
            self._print_start()

        self.picks = []
        for deck in self.decks:
            pick: int = deck.pop(0)
            self.picks.append(pick)
        if verbose:
            self._print_picks()

        self.winner: int = 0 if self.picks[0] > self.picks[1] else 1
        self.decks[self.winner].extend(reversed(sorted(self.picks)))

        if verbose:
            self._print_winner()
            print("")


def part_one(game: Game, verbose: bool = False) -> int:
    player, score = game.play_game(verbose)
    return score


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Advent of Code - 2020 - Day 22 - Crab Combat.")
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help='The puzzle input.  (Default "%(default)s")',
    )
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Increase output verbosity.",
    )
    args = parser.parse_args()

    try:
        with open(args.input, "rt") as inf:
            game = Game.parse_puzzle(inf.read())
        print(part_one(game, args.verbose))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
