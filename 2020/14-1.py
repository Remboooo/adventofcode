import re
from argparse import ArgumentParser

from util import timed


class Machine:
    def __init__(self):
        self.mem = {}
        self.mask_bits = 0
        self.mask_value = 0

    def write(self, address, value):
        value &= ~self.mask_bits
        value |= self.mask_value
        self.mem[address] = value

    def set_mask(self, mask):
        self.mask_bits = int(''.join('0' if c == 'X' else '1' for c in mask), 2)
        self.mask_value = int(''.join(c if c != 'X' else '0' for c in mask), 2)


LINE_PATTERNS = [
    (
        re.compile(r'^mem\[(\d+)] = (\d+)$'),
        lambda machine, match: Machine.write(machine, int(match.group(1)), int(match.group(2)))
    ),
    (
        re.compile(r'^mask = ([X10]{36})$'),
        lambda machine, match: Machine.set_mask(machine, match.group(1))
    ),
]


def run_instructions(f):
    machine = Machine()
    for line in f:
        for pattern, function in LINE_PATTERNS:
            match = pattern.fullmatch(line.strip())
            if match:
                function(machine, match)
                break
        else:
            raise ValueError(f"Cannot interpret line: {line}")
    return machine.mem


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="14-input.txt")
    args = argparse.parse_args()

    with open(args.file, "r") as f:
        mem = run_instructions(f)

    print(sum(mem.values()))


if __name__ == '__main__':
    main()
