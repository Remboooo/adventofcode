from argparse import ArgumentParser

from util import timed


DIRECTIONS = [
    (+1, 0),
    (0, -1),
    (-1, 0),
    (0, +1)
]


INSTRUCTIONS = {
    'N': lambda x, y, d, v: (x, y + v, d),
    'E': lambda x, y, d, v: (x + v, y, d),
    'S': lambda x, y, d, v: (x, y - v, d),
    'W': lambda x, y, d, v: (x - v, y, d),
    'L': lambda x, y, d, v: (x, y, (d - v//90) % 4),
    'R': lambda x, y, d, v: (x, y, (d + v//90) % 4),
    'F': lambda x, y, d, v: (x + v * DIRECTIONS[d][0], y + v * DIRECTIONS[d][1], d)
}


def read_instruction(stripped):
    return INSTRUCTIONS[stripped[0]], int(stripped[1:])


@timed
def execute(instructions):
    x, y, d, = 0, 0, 0
    for instruction, value in instructions:
        x, y, d = instruction(x, y, d, value)
    return x, y, d


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="12-input.txt")
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        instructions = [read_instruction(stripped) for stripped in [l.strip() for l in f] if stripped]

    x, y, d = execute(instructions)
    print(f"{x},{y},{d}")
    print(f"{abs(x)+abs(y)}")


if __name__ == '__main__':
    main()
