from collections import defaultdict
from itertools import count

import datetime
import re
from argparse import ArgumentParser

INITIAL_REGEX = re.compile(r'initial state: ([.#]+)')
MUTATION_REGEX = re.compile(r'([.#]+) => ([.#])')


def get_initial(param):
    match = INITIAL_REGEX.fullmatch(param)
    if not match:
        raise ValueError("Invalid initial state: {}".format(param))
    return match[1]


def get_mutation(param):
    match = MUTATION_REGEX.fullmatch(param)
    if not match:
        raise ValueError("Invalid mutation: {}".format(param))
    return match[1], match[2]


def find_all(a_str, sub):
    start = 0
    while True:
        start = a_str.find(sub, start)
        if start == -1:
            return
        yield start
        start += 1


def process(initial, mutations):
    left = 0
    generation = 0
    state = initial

    alive_mutations = [match for match, result in mutations if result == '#']

    for generation in range(20):
        state = '....' + state + '....'
        left -= 4
        while state[:6] == '......':
            state = state[1:]
            left += 1
        while state[-6:] == '......':
            state = state[:-1]

        print("{}: ({}) {}".format(generation, left, state))

        new_state = []

        for i in range(len(state) - 5):
            if state[i:i+5] in alive_mutations:
                new_state.append('#')
            else:
                new_state.append('.')

        left += 2

        state = ''.join(new_state)

    print("{}: ({}) {}".format(generation, left, state))
    print(sum(n+left for n, c in enumerate(state) if c == '#'))


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    try:
        with open(args.file, 'r') as f:
            initial = get_initial(f.readline().strip())
            mutations = [get_mutation(l.strip()) for l in f if l.strip()]
            process(initial, mutations)
    except FileNotFoundError:
        process(args.file)


if __name__ == '__main__':
    main()
