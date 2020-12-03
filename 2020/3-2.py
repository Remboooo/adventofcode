import re
from argparse import ArgumentParser
from itertools import combinations

pass_re = re.compile(r'^([0-9]+)-([0-9]+) ([a-z]): ([a-z]+)$')


def how_many_trees(forest, dx, dy):
    trees = 0
    x = 0
    y = 0
    while y < len(forest):
        if forest[y][x % len(forest[y])] == '#':
            trees += 1
        x += dx
        y += dy
    return trees


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="3-input.txt")
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        forest = [line for line in [l.strip() for l in f] if line]

        print(
            how_many_trees(forest, 1, 1) *
            how_many_trees(forest, 3, 1) *
            how_many_trees(forest, 5, 1) *
            how_many_trees(forest, 7, 1) *
            how_many_trees(forest, 1, 2)
        )


if __name__ == '__main__':
    main()
