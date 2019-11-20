#!/usr/bin/env python


import sys

import numpy as np


GRID_SERIAL_NUMBER = 5093


def power_level(x, y):
    rack_id = x + 10
    power = rack_id * y            # rack id * Y coordinate
    power += GRID_SERIAL_NUMBER    # increase by grid serial number
    power *= rack_id               # multiply by rack id
    power = (power % 1000) // 100  # save only hundreds digit
    power -= 5                     # subtract 5
    return power


def racks(grid, cx, cy):
    xm, ym = grid.shape
    for row in range(0, (ym - cy) + 1):
        for col in range(0, (xm - cx) + 1):
            yield grid[row:row + cy, col:col + cx], row, col


def part_one():
    grid = np.fromfunction(np.vectorize(power_level), (300, 300))

    max_power = -sys.maxsize
    max_rack = None
    for rack, row, col in racks(grid, 3, 3):
        power = sum(rack)
        if power > max_power:
            max_power = power
            max_rack = (col, row)

    return (max_power, max_rack)


if __name__ == "__main__":

    #print(power_level(8, Rack(3, 5)))
    #print(power_level(57, Rack(122, 79)))
    #print(power_level(39, Rack(217, 196)))
    #print(power_level(71, Rack(101, 153)))

    (power, rack) = part_one()
    print(f"{rack[0]},{rack[1]} {power}")
