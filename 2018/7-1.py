import re
from argparse import ArgumentParser
import numpy as np

DEP_REGEX = re.compile(r'Step ([A-Z]) must be finished before step ([A-Z]) can begin\.')


def dependency(s):
    match = DEP_REGEX.fullmatch(s.strip())
    if not match:
        raise ValueError("Not a valid dependency: {}".format(s))
    return match[1], match[2]


def process(data):
    steps = {s for row in data for s in row}
    do_first = {step: set() for step in steps}
    for finish, before in data:
        do_first[before].add(finish)

    sequence = []

    while True:
        print(do_first)
        can_do_now = sorted({step for step, deps in do_first.items() if not deps})
        if not can_do_now:
            break
        else:
            do_now = can_do_now[0]
            sequence.append(do_now)
            print(sequence)
            del do_first[do_now]
            for deps in do_first.values():
                deps.discard(do_now)

    print(''.join(sequence))


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    with open(args.file, 'r') as f:
        data = [dependency(s) for s in f]
        process(data)


if __name__ == '__main__':
    main()
