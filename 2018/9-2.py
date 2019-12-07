from itertools import count

import re
from argparse import ArgumentParser
import numpy as np

GAME_REGEX = re.compile(r'(\d+) players; last marble is worth (\d+) points')


def game_spec(s):
    match = GAME_REGEX.match(s.strip())
    if not match:
        raise ValueError("Not a valid spec: {}".format(s))
    return int(match[1]), int(match[2])


def process(data):
    num_players, last_worth = game_spec(data)
    last_worth *= 100

    circle = [0]
    current_marble_i = 0
    next_marble = 1
    next_player = 0

    scores = [0] * num_players

    for turn in count():
        if turn % 100000 == 0:
            print("{} / {} = {:%}".format(turn, last_worth, turn/last_worth))

        if next_marble % 23 == 0:
            score = next_marble
            pop_index = (current_marble_i - 7) % len(circle)
            score += circle.pop(pop_index)
            current_marble_i = pop_index % len(circle)

            scores[next_player] += score
        else:
            insert_index = (current_marble_i + 2) % len(circle)
            circle.insert(insert_index, next_marble)
            current_marble_i = insert_index

        if next_marble == last_worth:
            break

        next_marble += 1
        next_player = (next_player + 1) % num_players

    print("High score {}".format(max(scores)))


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    try:
        with open(args.file, 'r') as f:
            process(f.readline())
    except FileNotFoundError:
        process(args.file)


if __name__ == '__main__':
    main()
