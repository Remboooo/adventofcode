from argparse import ArgumentParser
import re
from functools import cache

line_re = re.compile(r"^Card *(\d+): (.+)$")
spaces_re = re.compile(r" +")

if __name__ == '__main__':
    argparse = ArgumentParser()
    argparse.add_argument("input", type=str)
    args = argparse.parse_args()

    wins = []

    with open(args.input, 'r') as f:
        while line := f.readline():
            match = line_re.match(line.strip())
            card_nr = int(match.group(1))
            winning_str, have_str = match.group(2).split(" | ")
            winning = [int(v) for v in spaces_re.split(winning_str) if v]
            have = [int(v) for v in spaces_re.split(have_str) if v]
            have_winning = [v for v in have if v in winning]
            wins.append(len(have_winning))

    @cache
    def count_cards(first, count):
        return count + sum(count_cards(x+1, wins[x]) for x in range(first, first+count))

    print(count_cards(0, len(wins)))
