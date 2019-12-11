# -*- coding: utf-8 -*-


import unittest

from solve import Bot, Direction, Turn


class BotUnitTests(unittest.TestCase):
    def test_turn_and_move_left(self):
        bot = Bot()
        self.assertEqual(bot.direction, Direction.NORTH)
        self.assertEqual(bot.position, (0, 0))

        bot.turn_and_move(Turn.LEFT)
        self.assertEqual(bot.direction, Direction.WEST)
        self.assertEqual(bot.position, (-1, 0))

        bot.turn_and_move(Turn.LEFT)
        self.assertEqual(bot.direction, Direction.SOUTH)
        self.assertEqual(bot.position, (-1, 1))

        bot.turn_and_move(Turn.LEFT)
        self.assertEqual(bot.direction, Direction.EAST)
        self.assertEqual(bot.position, (0, 1))

        bot.turn_and_move(Turn.LEFT)
        self.assertEqual(bot.direction, Direction.NORTH)
        self.assertEqual(bot.position, (0, 0))

    def test_turn_and_move_right(self):
        bot = Bot()
        self.assertEqual(bot.direction, Direction.NORTH)
        self.assertEqual(bot.position, (0, 0))

        bot.turn_and_move(Turn.RIGHT)
        self.assertEqual(bot.direction, Direction.EAST)
        self.assertEqual(bot.position, (1, 0))

        bot.turn_and_move(Turn.RIGHT)
        self.assertEqual(bot.direction, Direction.SOUTH)
        self.assertEqual(bot.position, (1, 1))

        bot.turn_and_move(Turn.RIGHT)
        self.assertEqual(bot.direction, Direction.WEST)
        self.assertEqual(bot.position, (0, 1))

        bot.turn_and_move(Turn.RIGHT)
        self.assertEqual(bot.direction, Direction.NORTH)
        self.assertEqual(bot.position, (0, 0))


if __name__ == "__main__":
    unittest.main()
