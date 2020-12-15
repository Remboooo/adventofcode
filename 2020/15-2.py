from argparse import ArgumentParser
from itertools import islice

from util import timed


def play(starting_numbers, count):
    # Using -1 in stead of None allows pypy3 to optimize this to an int array, saves a factor of 5 in runtime (!)
    history = [-1] * (count + 1)
    for turn, value in enumerate(starting_numbers):
        yield value
        history[value] = turn + 1

    last_number = starting_numbers[-1]

    for turn in range(len(starting_numbers), count):
        last_turn = history[last_number]
        if last_turn != -1:
            number = turn - last_turn
        else:
            number = 0
        history[last_number] = turn
        yield number
        last_number = number

    return last_number


@timed
def get_nth_number(gen, num):
    return next(islice(gen, num - 1, None))


def main():
    argparse = ArgumentParser()
    argparse.add_argument("input", nargs='?', type=str, default="14,1,17,0,3,20")
    argparse.add_argument("--verbose", "-v", action='store_true', help="Show intermediate results")
    argparse.add_argument("-n", nargs='?', type=int, default=30000000, help="Number of turns to play")
    args = argparse.parse_args()

    starting_numbers = [int(n.strip()) for n in args.input.split(',')]

    if args.verbose:
        for turn, number in enumerate(islice(play(starting_numbers, args.n), 0, args.n)):
            print(f"{turn:10d}: {number:10d}")
    else:
        print(get_nth_number(play(starting_numbers, args.n), args.n))


if __name__ == '__main__':
    main()
