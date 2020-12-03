import re
from argparse import ArgumentParser
from itertools import combinations

pass_re = re.compile(r'^([0-9]+)-([0-9]+) ([a-z]): ([a-z]+)$')


def how_many_trees_3right_1down(forest):
    trees = 0
    x = 0
    y = 0
    while y < len(forest):
        if forest[y][x % len(forest[y])] == '#':
            trees += 1
        x += 3
        y += 1
    return trees


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="3-input.txt")
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        forest = [line for line in [l.strip() for l in f] if line]
        print(how_many_trees_3right_1down(forest))


if __name__ == '__main__':
    main()
