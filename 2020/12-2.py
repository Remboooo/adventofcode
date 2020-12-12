import numpy as np
from argparse import ArgumentParser
from util import timed


INSTRUCTIONS = {
    'N': lambda wx, wy, sx, sy, v: (wx, wy + v, sx, sy),
    'E': lambda wx, wy, sx, sy, v: (wx + v, wy, sx, sy),
    'S': lambda wx, wy, sx, sy, v: (wx, wy - v, sx, sy),
    'W': lambda wx, wy, sx, sy, v: (wx - v, wy, sx, sy),
    'L': lambda wx, wy, sx, sy, v: (*(np.dot((wx, wy), np.linalg.matrix_power(((0, 1), (-1, 0)), v//90))), sx, sy),
    'R': lambda wx, wy, sx, sy, v: (*(np.dot((wx, wy), np.linalg.matrix_power(((0, -1), (1, 0)), v//90))), sx, sy),
    'F': lambda wx, wy, sx, sy, v: (wx, wy, sx + v * wx, sy + v * wy)
}


def read_instruction(stripped):
    return INSTRUCTIONS[stripped[0]], int(stripped[1:])


@timed
def execute(instructions):
    # Waypoint XY relative to ship, ship XY relative to start
    wx, wy, sx, sy, = 10, 1, 0, 0
    for instruction, value in instructions:
        wx, wy, sx, sy = instruction(wx, wy, sx, sy, value)
    return wx, wy, sx, sy


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="12-input.txt")
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        instructions = [read_instruction(stripped) for stripped in [l.strip() for l in f] if stripped]

    wx, wy, sx, sy = execute(instructions)
    print(f"{wx},{wy},{sx},{sy}")
    print(f"{abs(sx)+abs(sy)}")


if __name__ == '__main__':
    main()
