from collections import defaultdict

import re
from functools import reduce

from argparse import ArgumentParser

CLAIM_REGEX = re.compile(r'#(\d+) @ (\d+),(\d+): (\d+)x(\d+)')


def process(data):
    pixels = defaultdict(lambda: defaultdict(int))
    for num, left, top, width, height in data:
        for x in range(left, left+width):
            for y in range(top, top+height):
                pixels[x][y] += 1

    def has_only_one_claim(height, left, pixels, top, width):
        for x in range(left, left + width):
            for y in range(top, top + height):
                if pixels[x][y] > 1:
                    return False
        return True

    for num, left, top, width, height in data:
        if has_only_one_claim(height, left, pixels, top, width):
            print(num)


def claim(s):
    match = CLAIM_REGEX.fullmatch(s)
    return int(match[1]), int(match[2]), int(match[3]), int(match[4]), int(match[5])


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        data = [claim(l.strip()) for l in f]
    process(data)


if __name__ == '__main__':
    main()

