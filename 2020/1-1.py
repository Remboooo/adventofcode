from argparse import ArgumentParser
from itertools import combinations


def find_mult_2020(vals):
    for v1, v2 in combinations(vals, 2):
        if v1 + v2 == 2020:
            return v1 * v2


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="1-input.txt")
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        print(find_mult_2020([int(l) for l in f]))


if __name__ == '__main__':
    main()
