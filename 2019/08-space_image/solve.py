# -*- coding: utf-8 -*-

import argparse
import pdb
import traceback
from dataclasses import dataclass
from typing import List, Tuple

Layer = List[List[int]]


@dataclass
class Bitmap:
    width: int
    height: int
    layer: Layer

    @classmethod
    def from_image(cls, image):
        bitmap = Bitmap(image.width, image.height, [])
        bitmap.layer = [[None] * image.width for _ in range(image.height)]
        for layer in reversed(image.layers):
            for row in range(bitmap.height):
                for col in range(bitmap.width):
                    if layer[row][col] != 2:
                        bitmap.layer[row][col] = layer[row][col]
        return bitmap

    def dump(self) -> None:
        for row in range(self.height):
            for col in range(self.width):
                print(("\u2588", "\u2591")[self.layer[row][col]], end="")
            print("")


@dataclass
class Image:
    width: int
    height: int
    layers: List[Layer]
    num_layers: int = 0

    @classmethod
    def from_pixels(cls, pixels: List[int], width: int, height: int):
        image = Image(width, height, [])
        image.num_layers = len(pixels) // (width * height)
        for l in range(image.num_layers):
            layer: Layer = []
            for row in range(height):
                start: int = l * width * height + width * row
                layer.append(pixels[start : start + width])
            image.layers.append(layer[:])
        return image

    def count_pixels_per_layer(self, target: int) -> List[int]:
        totals: List[int] = []
        for idx, layer in enumerate(self.layers):
            total: int = 0
            for row in layer:
                total += row.count(target)
            totals.append(total)
        return totals

    def dump_layer(self, idx: int) -> None:
        layer = self.layers[idx]
        for row in range(self.height):
            for col in range(self.width):
                print(layer[row][col], end="")
            print("")


def solve(pixels: List[int], width: int, height: int) -> Tuple[int, int]:
    image: Image = Image.from_pixels(pixels, width, height)

    zeros_per_layer = image.count_pixels_per_layer(0)
    min_zero_layer = zeros_per_layer.index(min(zeros_per_layer))

    ones_per_layer = image.count_pixels_per_layer(1)
    twos_per_layer = image.count_pixels_per_layer(2)

    one: int = ones_per_layer[min_zero_layer] * twos_per_layer[min_zero_layer]

    two: int = -1
    bitmap: Bitmap = Bitmap.from_image(image)
    bitmap.dump()

    return (one, two)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Advent of Code - 2019 - Day 8 - Space Image Format."
    )
    parser.add_argument(
        "input",
        type=str,
        default="input.txt",
        nargs="?",
        help="The puzzle input.  (Default %(default)s)",
    )
    parser.add_argument(
        "width",
        type=int,
        default=25,
        nargs="?",
        help="The width of the image.  (Default %(default)s)",
    )
    parser.add_argument(
        "height",
        type=int,
        default=6,
        nargs="?",
        help="The height of the image.  (Default %(default)s)",
    )
    args = parser.parse_args()

    pixels: List[int] = []
    with open(args.input) as inf:
        for line in inf:
            pixels += list(map(int, list(line.strip())))
    try:
        print(solve(pixels, args.width, args.height))
    except Exception:
        traceback.print_exc()
        pdb.post_mortem()
