from argparse import ArgumentParser
from collections import defaultdict
from itertools import islice, count

from util import timed


def parse_rules(f):
    rules = {}
    for line in f:
        line = line.strip()
        if line == "":
            break
        name, values = line.split(": ", 1)
        ranges = values.split(" or ")
        ranges = [tuple(int(v) for v in r.split("-", 1)) for r in ranges]
        rules[name] = ranges
    return rules


def parse_my_ticket(f):
    for line in f:
        if line.strip() == "":
            break


def parse_tickets(f):
    if f.readline().strip() != "nearby tickets:":
        raise ValueError("First line was not 'nearby tickets'")

    for line in f:
        line = line.strip()
        yield tuple(int(field) for field in line.split(','))


def get_error_rate(nearby_tickets, rules):
    return sum(
        field if not any(r[0] <= field <= r[1] for rule in rules.values() for r in rule) else 0
        for ticket in nearby_tickets
        for field in ticket
    )


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="16-input.txt")
    args = argparse.parse_args()

    with open(args.file, 'r') as f:
        rules = parse_rules(f)
        my_ticket = parse_my_ticket(f)
        nearby_tickets = list(parse_tickets(f))

    print(rules)
    print(nearby_tickets)
    print(get_error_rate(nearby_tickets, rules))


if __name__ == '__main__':
    main()
