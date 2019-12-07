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


def process(nrecipes):
    recipes = [3, 7]
    elf_recipes = [0, 1]

    while len(recipes) < nrecipes + 10:
        #print_state(recipes, elf_recipes)
        score = sum(recipes[n] for n in elf_recipes)
        recipes += reversed(list(get_digits(score)))
        elf_recipes = [(e + 1 + recipes[e]) % len(recipes) for e in elf_recipes]

    print("Result: " + "".join(str(n) for n in recipes[nrecipes:nrecipes+10]))


if __name__ == '__main__':
    argparse = ArgumentParser()
    argparse.add_argument("nrecipes", type=int)
    args = argparse.parse_args()
    process(args.nrecipes)
