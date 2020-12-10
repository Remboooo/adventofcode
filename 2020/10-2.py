from argparse import ArgumentParser
from util import timed, memoized


@memoized(0)
def count_arrangements(current, target, adapters):
    if target - current <= 3:
        return 1
    else:
        return sum(
            count_arrangements(current + diff, target, adapters)
            for diff in range(1, 4)
            if current + diff in adapters
        )


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="10-input.txt")
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        adapters = {int(stripped) for stripped in (line.strip() for line in f) if stripped}

    arrangements = timed(count_arrangements)(0, max(adapters) + 3, adapters)
    print(arrangements)


if __name__ == '__main__':
    main()
