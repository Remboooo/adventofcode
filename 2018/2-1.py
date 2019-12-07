from collections import defaultdict
from functools import reduce

from argparse import ArgumentParser


def process(data):
    counts = defaultdict(int)
    for box in data:
        for letter_count in {box.count(letter) for letter in set(box)}:
            if letter_count > 1:
                counts[letter_count] += 1
    print(reduce(lambda a, b: a * b, counts.values(), 1))


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        data = [l.strip() for l in f]
    process(data)


if __name__ == '__main__':
    main()

