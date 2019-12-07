from argparse import ArgumentParser
from collections import defaultdict


def get_centers(orbiter, orbiter_to_center):
    if orbiter in orbiter_to_center:
        center = orbiter_to_center[orbiter]
        return [center] + get_centers(center, orbiter_to_center)
    else:
        return []


def get_common_center(santa_centers, you_centers):
    for sc in santa_centers:
        if sc in you_centers:
            return sc


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

    santa_centers = get_centers("SAN", orbiter_to_center)
    you_centers = get_centers("YOU", orbiter_to_center)
    common_center = get_common_center(santa_centers, you_centers)

    print(santa_centers.index(common_center) + you_centers.index(common_center))


if __name__ == '__main__':
    main()
