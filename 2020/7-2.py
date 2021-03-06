import regex
from argparse import ArgumentParser

# re module does not support retrieving repeated captures for groups
from util import timed

rule_re = regex.compile(r'^([a-z]+ [a-z]+) bags contain (?:(?:(?:([0-9]+) ([a-z]+ [a-z]+) bags?, )*([0-9]+) ([a-z]+ [a-z]+) bags?\.)|(?:no other bags\.))$')


def parse_rules(lines):
    rules = {}
    for line in lines:
        line = line.strip()
        if not line:
            continue
        match = rule_re.fullmatch(line)
        if not match:
            raise ValueError(f"Not a valid rule: {line}")
        bags = [bag for n in [3, 5] for bag in match.captures(n)]
        counts = [int(count) for n in [2, 4] for count in match.captures(n)]
        rules[match.group(1)] = {bag: count for bag, count in zip(bags, counts)}
    return rules


def find_needed_bags(container, rules):
    return sum(
        count + count * find_needed_bags(contained_bag, rules)
        for contained_bag, count in rules[container].items()
    )


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="7-input.txt")
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        rules = parse_rules(f)
        print(timed(find_needed_bags)('shiny gold', rules))


if __name__ == '__main__':
    main()
