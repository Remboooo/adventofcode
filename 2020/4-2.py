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


def check_height(v):
    if v[-2:] == 'cm':
        return 150 <= int(v[:-2]) <= 193
    elif v[-2:] == 'in':
        return 59 <= int(v[:-2]) <= 76


def is_valid(passport):
    validators = {
        'byr': lambda v: 1920 <= int(v) <= 2002,
        'iyr': lambda v: 2010 <= int(v) <= 2020,
        'eyr': lambda v: 2020 <= int(v) <= 2030,
        'hgt': check_height,
        'hcl': lambda v: re.fullmatch(r'^#[0-9a-f]{6}$', v),
        'ecl': lambda v: v in ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth'),
        'pid': lambda v: re.fullmatch(r'^[0-9]{9}$', v),
    }
    try:
        return all(field in passport and validator(passport[field]) for field, validator in validators.items())
    except ValueError:
        return False


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
