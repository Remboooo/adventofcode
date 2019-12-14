from argparse import ArgumentParser
from collections import defaultdict

import numpy as np
from intvm import IntVM
from util import IterableQueue


class Container:
    def __init__(self, value):
        self.value = value


class RobotIO:
    _sentinel = -1

    PAINTING = 0
    MOVING = 1

    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    DIRECTIONS = {
        UP: (0, -1),
        RIGHT: (1, 0),
        DOWN: (0, 1),
        LEFT: (-1, 0)
    }

    def __init__(self):
        self.pos = (0, 0)
        self.tiles = defaultdict(int)
        self.state = self.PAINTING
        self.direction = self.UP

    def __iter__(self):
        return iter(self.get_current_tile, self._sentinel)

    def get_current_tile(self):
        return self.tiles[self.pos]

    def output(self, value):
        if self.state == self.PAINTING:
            self.tiles[self.pos] = value
            self.state = self.MOVING
        elif self.state == self.MOVING:
            if value == 0:
                self.direction = (self.direction - 1) % 4
            elif value == 1:
                self.direction = (self.direction + 1) % 4

            self.pos = self.pos[0] + self.DIRECTIONS[self.direction][0], self.pos[1] + self.DIRECTIONS[self.direction][1]
            self.state = self.PAINTING

    def show_tiles(self):
        minx = min(x for x, y in self.tiles.keys())
        miny = min(y for x, y in self.tiles.keys())
        maxx = max(x for x, y in self.tiles.keys())
        maxy = max(y for x, y in self.tiles.keys())

        w = maxx - minx + 1
        h = maxy - miny + 1

        painting = np.zeros((w, h), dtype=int)

        for (x, y), color in self.tiles.items():
            painting[x-minx, y-miny] = color

        for y in range(h):
            print(''.join('#' if color else ' ' for color in painting[:, y]))


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str, nargs="?", default="11-input.txt")
    args = argparse.parse_args()

    with open(args.file, "r") as f:
        program = [int(c) for c in f.read().split(',')]

    robot = RobotIO()
    robot.tiles[(0, 0)] = 1

    IntVM(program, robot, robot.output).run()

    robot.show_tiles()


if __name__ == '__main__':
    main()
