# -*- coding: utf-8 -*-


import unittest

from solve1 import Moon, Vector, apply_gravity


class VectorUnitTests(unittest.TestCase):
    def test_constructor(self):
        v = Vector()
        self.assertEqual(v.x, 0)
        self.assertEqual(v.y, 0)
        self.assertEqual(v.z, 0)

        v = Vector.parse("<x=-1, y=0, z=2>")
        self.assertEqual(v, Vector(-1, 0, 2))

        v = Vector.parse("<x=2, y=-10, z=-7>")
        self.assertEqual(v, Vector(2, -10, -7))

        v = Vector.parse("<x=4, y=-8, z=8>")
        self.assertEqual(v, Vector(4, -8, 8))

        v = Vector.parse("<x=3, y=5, z=-1>")
        self.assertEqual(v, Vector(3, 5, -1))

        v = Vector.parse("<x=128, y=256, z=-512>")
        self.assertEqual(v, Vector(128, 256, -512))


class MoonUnitTests(unittest.TestCase):
    def test_constructor(self):
        m = Moon.parse("<x=-1, y=0, z=2>")
        self.assertEqual(m, Moon(Vector(-1, 0, 2), Vector(0, 0, 0)))

    def test_apply_gravity(self):
        ganymede = Moon.parse("<x=3, y=3, z=10>")
        callisto = Moon.parse("<x=5, y=3, z=1>")

        ganymede.apply_gravity(callisto)
        self.assertEqual(ganymede.vel, Vector(1, 0, -1))

        callisto.apply_gravity(ganymede)
        self.assertEqual(callisto.vel, Vector(-1, 0, 1))

    def test_apply_velocity(self):
        europa = Moon(Vector(1, 2, 3), Vector(-2, 0, 3))
        europa.apply_velocity()
        self.assertEqual(europa.pos, Vector(-1, 2, 6))


class SolutionUnitTests(unittest.TestCase):
    def test_apply_gravity_2(self):
        moons = [Moon(Vector(0, 0, 0), Vector(0, 0, 0)), Moon(Vector(9, 9, 9), Vector(3, 3, 3))]
        apply_gravity(moons)
        self.assertEqual(moons[0].vel, Vector(1, 1, 1))
        self.assertEqual(moons[1].vel, Vector(2, 2, 2))

    def test_apply_gravity_3(self):
        moons = [
            Moon(Vector(0, 0, 0), Vector(0, 0, 0)),
            Moon(Vector(4, 4, 4), Vector(2, 2, 2)),
            Moon(Vector(9, 9, 9), Vector(3, 3, 3)),
        ]
        apply_gravity(moons)
        self.assertEqual(moons[0].vel, Vector(2, 2, 2))
        self.assertEqual(moons[1].vel, Vector(2, 2, 2))
        self.assertEqual(moons[2].vel, Vector(1, 1, 1))


if __name__ == "__main__":
    unittest.main()
