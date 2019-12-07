from argparse import ArgumentParser
from itertools import combinations_with_replacement


def main():
    argparse = ArgumentParser()
    argparse.add_argument("input", type=str, nargs='?', default="138307-654504")
    args = argparse.parse_args()

    rmin, rmax = [int(p) for p in args.input.split('-')]

    result_set = set()

    for digits in combinations_with_replacement((str(s) for s in range(10)), 5):
        for repeat_pos in range(5):
            combo = list(digits)
            combo[repeat_pos] = combo[repeat_pos]+combo[repeat_pos]
            candidate = int(''.join(combo))
            if rmin <= candidate <= rmax:
                result_set.add(candidate)

    print(len(result_set))


if __name__ == '__main__':
    main()
