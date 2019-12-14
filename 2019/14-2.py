from argparse import ArgumentParser
from collections import defaultdict
from math import ceil


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
    argparse.add_argument("--graph", action="store_true")
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        reactions = [parse_reaction(l.strip()) for l in f.readlines()]

    output_to_reaction = {}
    for reaction in reactions:
        inputs, (output_amount, output_stuff) = reaction
        output_to_reaction[output_stuff] = reaction

    stuffs = set(stuff for _, (_, stuff) in reactions)
    stuffs.update(input_stuff for inputs, (_, stuff) in reactions for _, input_stuff in inputs)

    stuff_amounts = {stuff: 0 for stuff in stuffs}

    if args.graph:
        output_graph(reactions, stuffs)
        return

    num_try_fuel_produce = 1000000
    produced_fuel = 0

    while True:
        new_stuff_amounts = produce_fuel(num_try_fuel_produce, output_to_reaction, stuff_amounts)
        if new_stuff_amounts["ORE"] >= -1000000000000:
            produced_fuel += num_try_fuel_produce
            stuff_amounts = new_stuff_amounts
            print("{} fuel => ore: {}, fuel: {}".format(num_try_fuel_produce, -stuff_amounts["ORE"], produced_fuel))
        else:
            if num_try_fuel_produce > 1:
                num_try_fuel_produce = max(1, num_try_fuel_produce // 2)
            else:
                break

    for stuff, amount in stuff_amounts.items():
        print("{}: {}".format(stuff, amount))
    print("Fuel produceable: {}".format(produced_fuel))


def output_graph(reactions, stuffs):
    with open("graph.dot", "w") as f:
        f.write("digraph {\n")
        for stuff in stuffs:
            f.write(stuff)
            f.write(";\n")

        for inputs, (output_amount, output_stuff) in reactions:
            for input_amount, input_stuff in inputs:
                f.write("{} -> {};\n".format(input_stuff, output_stuff))

        f.write("}\n")


def produce_fuel(num_fuel, output_to_reaction, input_stuff_amounts):
    stuff_amounts = input_stuff_amounts.copy()
    stuff_amounts["FUEL"] = -num_fuel
    while any(v < 0 for stuff, v in stuff_amounts.items() if stuff != "ORE"):
        for stuff in stuff_amounts.keys():
            if stuff == "ORE":
                continue
            if stuff_amounts[stuff] < 0:
                reaction_inputs, (output_amount, output_stuff) = output_to_reaction[stuff]
                multiple = int(ceil(-stuff_amounts[stuff] / output_amount))

                output_amount *= multiple
                for input_amount, input_stuff in reaction_inputs:
                    input_amount *= multiple
                    stuff_amounts[input_stuff] -= input_amount
                stuff_amounts[stuff] += output_amount
    return stuff_amounts


if __name__ == '__main__':
    main()
