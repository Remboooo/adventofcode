from argparse import ArgumentParser
from functools import reduce


def read_groups(f):
    return [[set(line) for line in group.split('\n') if line] for group in f.read().split('\n\n')]


def get_all_yes_per_group(groups):
    for group in groups:
        yield reduce(lambda a, b: a & b, group[1:], group[0])


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="6-input.txt")
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        groups = read_groups(f)
        groups_or = list(get_all_yes_per_group(groups))
        print(sum(len(group) for group in groups_or))


if __name__ == '__main__':
    main()
