from collections import defaultdict

import re
from functools import reduce

from argparse import ArgumentParser
from datetime import datetime, timedelta


def iterate(data):
    skip = False
    for a, b in zip(data[:-1], data[1:]):
        if skip:
            skip = False
            continue
        if a.isupper() != b.isupper() and a.lower() == b.lower():
            skip = True
        else:
            yield a
    if not skip:
        yield data[-1]


def process(data):
    new_data = None
    while new_data != data:
        data = new_data if new_data is not None else data
        print(len(data))
        new_data = ''.join(iterate(data))


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        data = f.readline().strip()
    process(data)


if __name__ == '__main__':
    main()

