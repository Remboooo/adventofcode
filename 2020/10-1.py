from argparse import ArgumentParser
from collections import defaultdict
from itertools import combinations

from util import timed


def find_1_2_3_jolt_steps(outputs):
    remaining_adapters = set(outputs)
    current = 0
    diff_counts = {0: 0, 1: 0, 2: 0, 3: 1}

    while remaining_adapters:
        for diff in range(1, 4):
            if current + diff in remaining_adapters:
                current += diff
                remaining_adapters.remove(current)
                diff_counts[diff] += 1
                break
        else:
            raise ValueError(f"Could not find step up from {current}. Remaining adapters: {remaining_adapters}")

    return diff_counts


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="10-input.txt")
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        adapters = [int(stripped) for stripped in (line.strip() for line in f) if stripped]

    distribution = timed(find_1_2_3_jolt_steps)(adapters)
    print(distribution)
    print(distribution[1] * distribution[3])


if __name__ == '__main__':
    main()
