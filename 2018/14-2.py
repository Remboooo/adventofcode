from argparse import ArgumentParser


def get_digits(num):
    while num > 9:
        yield num % 10
        num //= 10
    yield num


MARKERS = "()[]"


def print_state(recipes, elf_recipes):
    for i, r in enumerate(recipes):
        if i in elf_recipes:
            elf = elf_recipes.index(i)
            print("{}{}{}".format(MARKERS[2*elf], r, MARKERS[2*elf+1]), end='')
        else:
            print(" {} ".format(r), end='')
    print()


def process(sequence):
    recipes = [3, 7]
    elf_recipes = [0, 1]

    list_sequence = [int(c) for c in sequence]
    match = None

    while match is None:
        score = sum(recipes[n] for n in elf_recipes)
        recipes += reversed(list(get_digits(score)))
        elf_recipes = [(e + 1 + recipes[e]) % len(recipes) for e in elf_recipes]
        if recipes[-len(sequence):] == list_sequence:
            match = len(recipes) - len(sequence)
        elif recipes[-len(sequence) - 1:-1] == list_sequence:
            match = len(recipes) - len(sequence) - 1

    print("{} appears after {} recipes".format(sequence, match))


if __name__ == '__main__':
    argparse = ArgumentParser()
    argparse.add_argument("sequence", type=str)
    args = argparse.parse_args()
    process(args.sequence)
