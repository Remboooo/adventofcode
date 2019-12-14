from argparse import ArgumentParser
from collections import defaultdict


def parse_reaction(l):
    input_specs, output_spec = l.split(" => ")
    inputs = []
    for input_spec in input_specs.split(", "):
        amount, stuff = input_spec.split(" ")
        amount = int(amount)
        inputs.append((amount, stuff))

    output_amount, output_stuff = output_spec.split(" ")
    output_amount = int(output_amount)
    return inputs, (output_amount, output_stuff)


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str, nargs='?', default="14-input.txt")
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        reactions = [parse_reaction(l.strip()) for l in f.readlines()]

    output_to_reaction = {}
    for reaction in reactions:
        inputs, (output_amount, output_stuff) = reaction
        output_to_reaction[output_stuff] = reaction

    stuff_amounts = defaultdict(int)
    stuff_amounts["FUEL"] = -1

    needed_ore = 0

    while any(v < 0 for v in stuff_amounts.values()):
        for stuff, amount in list(stuff_amounts.items()):
            if amount < 0:
                reaction_inputs, (output_amount, output_stuff) = output_to_reaction[stuff]
                stuff_amounts[stuff] += output_amount
                for input_amount, input_stuff in reaction_inputs:
                    if input_stuff == "ORE":
                        needed_ore += input_amount
                    else:
                        stuff_amounts[input_stuff] -= input_amount

    print(needed_ore)


if __name__ == '__main__':
    main()
