from argparse import ArgumentParser
from collections import defaultdict
from functools import reduce
from itertools import islice, count
from pprint import pprint

from util import timed


def parse_rules(f):
    rules = {}
    for line in f:
        line = line.strip()
        if line == "":
            break
        name, values = line.split(": ", 1)
        rules[name] = [tuple(int(v) for v in r.split("-", 1)) for r in values.split(" or ")]
    return rules


def parse_my_ticket(f):
    if f.readline().strip() != "your ticket:":
        raise ValueError("First line was not 'your ticket:'")

    result = tuple(int(field) for field in f.readline().split(','))
    f.readline()
    return result


def parse_tickets(f):
    if f.readline().strip() != "nearby tickets:":
        raise ValueError("First line was not 'nearby tickets:'")

    for line in f:
        line = line.strip()
        yield tuple(int(field) for field in line.split(','))


@timed
def get_valid_tickets(nearby_tickets, rules):
    # A ticket is valid if *all* fields match *any* of the rules
    return [
        ticket for ticket in nearby_tickets
        if all(any(rlow <= field <= rhigh for rule in rules.values() for rlow, rhigh in rule) for field in ticket)
    ]


@timed
def find_field_ids(nearby_tickets, rules):
    field_ids = {}
    # For every field name in the rulebook, check which field IDs match its rules on all of the valid tickets
    for field_name, rule in rules.items():
        # Start by considering every possible field ID for this name
        possible_ids = set(range(len(nearby_tickets[0])))
        for ticket in nearby_tickets:
            # Prune the possible IDs for this field name by checking which field IDs match its rules on this ticket
            possible_ids &= {n for n, field in enumerate(ticket) if any(rlow <= field <= rhigh for rlow, rhigh in rule)}
        field_ids[field_name] = possible_ids

    # Some fields still have multiple possibilities after checking all of the tickets, but then others only have one,
    # so there's some overlap and we can eliminate the ambiguities.
    # I'm 99% sure this will not work in all possible cases, but it works for the test input and my puzzle input 🤷🏻‍
    field_ids = {
        name: next(
            fid for fid in pid
            if not any(
                # if there's another field with a shorter list of ID options that also contains this ID, skip it
                name != oname and len(opid) < len(pid) and fid in opid
                for oname, opid in field_ids.items()
            )
        )
        for name, pid in field_ids.items()
    }
    return field_ids


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="16-input.txt")
    args = argparse.parse_args()

    with open(args.file, 'r') as f:
        rules = parse_rules(f)
        my_ticket = parse_my_ticket(f)
        nearby_tickets = list(parse_tickets(f))

    nearby_tickets = get_valid_tickets(nearby_tickets, rules)
    field_ids = find_field_ids(nearby_tickets, rules)
    print(
        reduce(lambda a, b: a * b, (my_ticket[fid] for name, fid in field_ids.items() if name.startswith('departure')))
    )


if __name__ == '__main__':
    main()
