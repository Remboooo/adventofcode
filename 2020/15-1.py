from argparse import ArgumentParser
from collections import defaultdict
from itertools import islice, count

from util import timed


def play(starting_numbers):
    history = defaultdict(lambda: (None, None))

    last_number = None

    for turn, number in enumerate(starting_numbers):
        history[number] = turn, history[number][0]
        last_number = number
        yield number

    for turn in count(len(history)):
        prev, prevprev = history[last_number]

        if prevprev is None:
            number = 0
        else:
            number = prev - prevprev

        history[number] = turn, history[number][0]
        yield number
        last_number = number


@timed
def get_nth_number(gen, num):
    return next(islice(gen, num - 1, None))


def main():
    argparse = ArgumentParser()
    argparse.add_argument("input", nargs='?', type=str, default="14,1,17,0,3,20")
    argparse.add_argument("-n", nargs='?', type=int, default=2020, help="Number of turns to play")
    argparse.add_argument("--verbose", "-v", action='store_true', help="Show intermediate results")
    args = argparse.parse_args()

    starting_numbers = [int(n.strip()) for n in args.input.split(',')]

    if args.verbose:
        for turn, number in enumerate(islice(play(starting_numbers), 0, args.n)):
            print(f"{turn:10d}: {number:10d}")
    else:
        print(get_nth_number(play(starting_numbers), args.n))


if __name__ == '__main__':
    main()
