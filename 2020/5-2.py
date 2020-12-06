from argparse import ArgumentParser


def get_seat_id(spec):
    fb = {'F': 0, 'B': 1}
    lr = {'L': 0, 'R': 1}
    row = sum(fb[c] * (2**(6-i)) for i, c in enumerate(spec[:7]))
    col = sum(lr[c] * (2**(2-i)) for i, c in enumerate(spec[7:]))
    return 8*row + col


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="5-input.txt")
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        passes = set(get_seat_id(l.strip()) for l in f)
        missing_pass = next(
            candidate
            for candidate in range(max(passes))
            if candidate not in passes
            and candidate-1 in passes
            and candidate+1 in passes
        )

        print(missing_pass)


if __name__ == '__main__':
    main()
