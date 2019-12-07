from itertools import count
from time import sleep

import re
from argparse import ArgumentParser
from drawille import Canvas

SPEC_REGEX = re.compile(r'position=< *(-?[0-9]+), *(-?[0-9]+)> velocity=< *(-?[0-9]+), *(-?[0-9]+)>')


def spec(s):
    match = SPEC_REGEX.fullmatch(s)
    if not match:
        raise ValueError("Not a valid spec: {}".format(s))
    else:
        return (int(match[1]), int(match[2])), (int(match[3]), int(match[4]))


def minmax(param):
    param = list(param)
    return min(param), max(param)


def process(data):
    positions = [pos for pos, vel in data]
    velocities = [vel for pos, vel in data]

    prev_width, prev_height = None, None
    left, top = 0, 0
    best_positions = None

    while True:
        left, right = minmax(x for x, y in positions)
        top, bottom = minmax(y for x, y in positions)

        width, height = right-left, bottom-top

        if prev_width and width > prev_width and prev_height and height > prev_height:
            break
        else:
            prev_width, prev_height = width, height

        best_positions = positions.copy()

        for i, (dx, dy) in enumerate(velocities):
            x, y = positions[i]
            x += dx
            y += dy
            positions[i] = (x, y)

    c = Canvas()
    for x, y in best_positions:
        c.set(x - left, y - top)
    print(c.frame())


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    with open(args.file, 'r') as f:
            process([spec(l.strip()) for l in f])


if __name__ == '__main__':
    main()
