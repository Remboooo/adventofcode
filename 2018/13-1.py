from collections import defaultdict
from itertools import count

import datetime
import re
from argparse import ArgumentParser
from enum import Enum


class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3


DIRECTION_CHARS = "^>v<"
DIRECTION_DELTA = ((-1, 0), (0, 1), (1, 0), (0, -1))
TURN_STEPS = [-1, 0, 1]


def process(data):
    tracks, trains = get_tracks_trains(data)

    for iteration in count():
        print_state(iteration, tracks, trains)
        for i, (y, x, direction, turn_step) in enumerate(sorted(trains.copy())):
            dy, dx = DIRECTION_DELTA[direction.value]
            x += dx
            y += dy
            for j, (y2, x2, direction2, *_) in enumerate(trains):
                if i == j:
                    continue
                if x == x2 and y == y2:
                    print_state(iteration, tracks, [t for k, t in enumerate(trains) if k not in (i, j)], (y2, x2))
                    return
            if tracks[y][x] == "/":
                direction = Direction(direction.value ^ 1)
            elif tracks[y][x] == "\\":
                direction = Direction(direction.value ^ 3)
            elif tracks[y][x] == "+":
                direction = Direction((direction.value + TURN_STEPS[turn_step]) % 4)
                turn_step = (turn_step + 1) % len(TURN_STEPS)
            elif tracks[y][x] not in "-|":
                raise ValueError("Track stopped at {},{}?".format(x, y))
            trains[i] = (y, x, direction, turn_step)


def get_tracks_trains(data):
    trains = []
    for y, row in enumerate(data):
        for x, char in enumerate(row):
            direction = DIRECTION_CHARS.find(char)
            if direction != -1:
                trains.append((y, x, Direction(direction), 0))
    tracks = [["-" if c in "<>" else "|" if c in "^v" else c for c in row] for row in data]
    return tracks, trains


def print_state(iteration, tracks, trains, collision=None):
    print("Tick {}".format(iteration))
    tracks = [row.copy() for row in tracks]
    for y, x, direction, *_ in trains:
        tracks[y][x] = DIRECTION_CHARS[direction.value]
    if collision is not None:
        y, x = collision
        tracks[y][x] = 'X'
        print("Crash at {},{}".format(x, y))
    print("\n".join("".join(row) for row in tracks))

    print()


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    with open(args.file, 'r') as f:
            process([line.rstrip("\r\n") for line in f])


if __name__ == '__main__':
    main()
