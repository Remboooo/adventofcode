import curses
import sys
import time
from argparse import ArgumentParser

import numpy as np

from intvm import IntVM
from curses import wrapper


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str, nargs="?", default="16-input.txt")
    argparse.add_argument("--rounds", "-r", type=int, default=100)
    args = argparse.parse_args()

    with open(args.file, "r") as f:
        digits = [int(d) for d in f.readline().strip()]

    pattern = [0, 1, 0, -1]

    for round in range(args.rounds):
        digits = do_round(digits, pattern)
        print("{}: ".format(round+1) + ''.join(str(d) for d in digits[:8]))


def do_round(digits_in, pattern):
    digits_out = [0] * len(digits_in)
    for output_i in range(len(digits_in)):
        digits_out[output_i] = abs(sum(
            input_digit * pattern[((input_i+1)//(output_i+1)) % len(pattern)]
            for input_i, input_digit in enumerate(digits_in)
        )) % 10
    return digits_out


if __name__ == '__main__':
    main()
