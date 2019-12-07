from argparse import ArgumentParser
from collections import defaultdict


def get_num_orbits(center, center_to_orbiters, current_count=0):
    if center not in center_to_orbiters:
        return current_count
    else:
        return sum(
            get_num_orbits(orbiter, center_to_orbiters, current_count+1)
            for orbiter in center_to_orbiters[center]
        ) + current_count


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()

    orbiter_to_center = {}
    center_to_orbiters = defaultdict(set)

    with open(args.file, "r") as f:
        for line in f:
            center, orbiter = line.strip().split(")")
            center_to_orbiters[center].add(orbiter)
            orbiter_to_center[orbiter] = center

    print(center_to_orbiters)
    print(get_num_orbits("COM", center_to_orbiters))


if __name__ == '__main__':
    main()
