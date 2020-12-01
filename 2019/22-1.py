import re
from argparse import ArgumentParser

DEAL_NEW_STACK = 'deal into new stack'
CUT = re.compile(r'^cut (-?[0-9]+)$')
DEAL_WITH_INCREMENT = re.compile(r'^deal with increment ([0-9]+)')


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str, nargs="?", default="22-input.txt")
    argparse.add_argument("--cards", "-c", type=int, nargs="?", default=10007)
    args = argparse.parse_args()

    with open(args.file, "r") as f:
        instructions = [l.strip() for l in f.readlines()]

    num_cards = args.cards
    deck = list(range(num_cards))

    for instruction in instructions:
        if instruction == DEAL_NEW_STACK:
            deck = list(reversed(deck))
            continue

        cut_match = CUT.fullmatch(instruction)
        if cut_match:
            cut = int(cut_match.group(1))
            deck = deck[cut:] + deck[:cut]
            continue

        deal_match = DEAL_WITH_INCREMENT.fullmatch(instruction)
        if deal_match:
            increment = int(deal_match.group(1))
            new_deck = deck.copy()
            for n, card in enumerate(deck):
                new_deck[(n * increment) % num_cards] = card
            deck = new_deck

    if num_cards == 10007:
        # For puzzle input, print the answer
        print(deck.index(2019))
    else:
        # Otherwise, print the whole deck
        print(deck)


if __name__ == '__main__':
    main()
