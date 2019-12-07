from collections import defaultdict
from itertools import combinations

from functools import reduce

from argparse import ArgumentParser


def process(data):
    for box1, box2 in combinations(data, 2):
        if len(box1) != len(box2):
            continue
        common = ''.join(letter1 for letter1, letter2 in zip(box1, box2) if letter1 == letter2)
        if len(common) == len(box1) - 1:
            print(common)


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        data = [l.strip() for l in f]
    process(data)


if __name__ == '__main__':
    main()

