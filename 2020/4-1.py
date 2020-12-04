import re
from argparse import ArgumentParser
from itertools import combinations


def read_passports(f):
    current_passport = {}

    for line in f:
        line = line.strip()
        if not line:
            if current_passport:
                yield current_passport
                current_passport = {}
        else:
            for entry in line.split(' '):
                k, v = entry.split(':', 1)
                current_passport[k] = v

    if current_passport:
        yield current_passport


def is_valid(passport):
    return all(field in passport for field in ['byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl',' pid'])


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="4-input.txt")
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        passports = list(read_passports(f))
        num_valid = sum(1 for passport in passports if is_valid(passport))
        print(num_valid)


if __name__ == '__main__':
    main()
