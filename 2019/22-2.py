import re
from argparse import ArgumentParser
from itertools import count

STR_DEAL_NEW_STACK = 'deal into new stack'
RE_CUT = re.compile(r'^cut (-?[0-9]+)$')
RE_DEAL_WITH_INCREMENT = re.compile(r'^deal with increment ([0-9]+)')

DEAL = 1
CUT = 2
DEAL_INC = 3


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str, nargs="?", default="22-input.txt")
    argparse.add_argument("--cards", "-c", type=int, nargs="?", default=119315717514047)
    argparse.add_argument("--repetitions", "-r", type=int, nargs="?", default=101741582076661)
    argparse.add_argument("--position", "-p", type=int, nargs="?", default=2020)
    args = argparse.parse_args()

    with open(args.file, "r") as f:
        lines = [l.strip() for l in f.readlines()]

    def interpret(lines, num_cards):
        for line in lines:
            if line == STR_DEAL_NEW_STACK:
                yield (DEAL, None)
                continue

            cut_match = RE_CUT.fullmatch(line)
            if cut_match:
                yield (CUT, int(cut_match.group(1)))
                continue

            deal_inc_match = RE_DEAL_WITH_INCREMENT.fullmatch(line)
            if deal_inc_match:
                increment = int(deal_inc_match.group(1))
                # Precalculate the modular multiplicative inverse to save time; see below
                yield (DEAL_INC, pow(increment, -1, num_cards))  # NOTE: needs python 3.8
                continue


    num_cards = args.cards
    last_card = num_cards - 1
    result_pos = args.position
    reps = args.repetitions
    
    instructions = list(interpret(lines, num_cards))

    # We run backwards through the instructions to find out which input position ends up at the result position
    pos = result_pos

    intermediate_results = {}

    for reps in count():
        for step, (instruction, argument) in enumerate(reversed(instructions)):
            if pos in intermediate_results:
                print("{} == {}: {}".format(intermediate_results[pos], (reps, step), pos))
                ex = intermediate_results[pos]
                if isinstance(ex, list):
                    ex.append((reps, step))
                else:
                    intermediate_results[pos] = [ex, (reps, step)]
            else:
                intermediate_results[pos] = (reps, step)

            if instruction == DEAL:
                pos = last_card - pos

            elif instruction == CUT:
                cut = argument
                if cut < 0:
                    cut = num_cards + cut

                if pos < num_cards - cut:
                    pos += cut
                else:
                    pos -= num_cards - cut

            elif instruction == DEAL_INC:
                # solve for new_pos: (new_pos * increment) % num_cards = pos

                # First, find the modular multiplicative inverse of the increment modulo the number of cards,
                # so we know the number of times we need to deal before hitting position #1, that is:
                # solve for n: (n * increment) % num_cards = 1
                mod_mult_inverse = argument  # We precalculated this in the instruction interpretation step

                # Now that we now how many times to deal before hitting the first location, we just multiply this number
                # by the desired location modulo num_cards to get the input position (pos):
                pos = (mod_mult_inverse * pos) % num_cards



if __name__ == '__main__':
    main()
