from argparse import ArgumentParser
from collections import defaultdict

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


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()

    with open(args.file, "r") as f:
        program = [int(c) for c in f.read().split(',')]

    robot = RobotIO()

    IntVM(program, robot, robot.output).run()

    print(len(robot.tiles))


if __name__ == '__main__':
    main()
