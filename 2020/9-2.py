from argparse import ArgumentParser
from itertools import combinations, accumulate

from util import timed


@timed
def find_first_not_2sum(code, preamble_length=2):
    for n, num in enumerate(code[preamble_length:], preamble_length):
        for num1, num2 in combinations(code[max(0, n-preamble_length):n], 2):
            if num1 + num2 == num:
                break
        else:
            return num


@timed
def find_contiguous_number_sum(weak_sum, code):
    for start in range(len(code)):
        for end, running_sum in enumerate(accumulate(code[start:]), start+1):
            if running_sum == weak_sum:
                return code[start:end]


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="9-input.txt")
    argparse.add_argument("--preamble-length", "-p", type=int, default=25)
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        code = [int(stripped) for stripped in (line.strip() for line in f) if stripped]

    weak_sum = find_first_not_2sum(code, preamble_length=args.preamble_length)
    print(weak_sum)

    sum_range = find_contiguous_number_sum(weak_sum, code)
    print(sum_range)
    print(min(sum_range) + max(sum_range))


if __name__ == '__main__':
    main()
