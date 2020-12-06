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
        passes = list(get_seat_id(l.strip()) for l in f)
        print(max(passes))


if __name__ == '__main__':
    main()
