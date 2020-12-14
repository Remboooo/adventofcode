import re
from argparse import ArgumentParser
from itertools import combinations

from util import timed


class Machine:
    def __init__(self):
        self.mem = {}
        self.mask_or = 0
        self.mask_and = 2**36-1
        self.mask_floats = []

    def write(self, address, value):
        base_address = (address | self.mask_or) & self.mask_and
        self.mem[base_address] = value
        for num_combinations in range(1, 1 + len(self.mask_floats)):
            for combination in combinations(self.mask_floats, num_combinations):
                self.mem[base_address | sum(combination)] = value

    def set_mask(self, mask):
        self.mask_or = int(''.join('1' if c == '1' else '0' for c in mask), 2)
        self.mask_and = int(''.join('0' if c == 'X' else '1' for c in mask), 2)
        self.mask_floats = [2**(35-n) for n, c in enumerate(mask) if c == 'X']


LINE_PATTERNS = [
    (
        re.compile(r'^mem\[(\d+)] = (\d+)$'),
        lambda machine, data: Machine.write(machine, int(data[0]), int(data[1]))
    ),
    (
        re.compile(r'^mask = ([X10]{36})$'),
        lambda machine, data: Machine.set_mask(machine, data[0])
    ),
]


@timed
def run_instructions(instructions):
    machine = Machine()
    for instruction, groups in instructions:
        instruction(machine, groups)
    return machine.mem


def read_instructions(f):
    for line in f:
        for pattern, function in LINE_PATTERNS:
            match = pattern.fullmatch(line.strip())
            if match:
                yield function, match.groups()
                break
        else:
            raise ValueError(f"Cannot interpret line: {line}")


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="14-input.txt")
    args = argparse.parse_args()

    with open(args.file, "r") as f:
        instructions = list(read_instructions(f))

    mem = run_instructions(instructions)

    print(sum(mem.values()))


if __name__ == '__main__':
    main()
