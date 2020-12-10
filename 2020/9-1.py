from argparse import ArgumentParser
from itertools import combinations

from util import timed


def find_first_not_2sum(code, preamble_length=2):
    for n, num in enumerate(code[preamble_length:], preamble_length):
        for num1, num2 in combinations(code[max(0, n-preamble_length):n], 2):
            if num1 + num2 == num:
                break
        else:
            return num


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="9-input.txt")
    argparse.add_argument("--preamble-length", "-p", type=int, default=25, help="Use 5 for test input")
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        code = [int(stripped) for stripped in (line.strip() for line in f) if stripped]

    print(timed(find_first_not_2sum)(code, preamble_length=args.preamble_length))


if __name__ == '__main__':
    main()
