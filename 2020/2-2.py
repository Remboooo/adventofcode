import re
from argparse import ArgumentParser
from itertools import combinations

pass_re = re.compile(r'^([0-9]+)-([0-9]+) ([a-z]): ([a-z]+)$')


def get_valid_passwords(lines):
    for line in lines:
        match = pass_re.fullmatch(line)
        if not match:
            raise ValueError(f"Corrupt line: {line}")
        indices = int(match[1]), int(match[2])
        required = match[3]
        password = match[4]

        if len([1 for letter in (password[i - 1] for i in indices) if letter == required]) == 1:
            yield password


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="2-input.txt")
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        valid = list(get_valid_passwords([l.strip() for l in f]))
        print(valid)
        print(len(valid))


if __name__ == '__main__':
    main()
