from argparse import ArgumentParser
import numpy as np


def location(s):
    a, b = s.split(', ')
    return int(a), int(b)


def distance_grid(loc, width, height):
    cx, cy = loc
    ys = np.array([abs(y - cy) for y in range(height)]).reshape(height, 1)
    xs = np.array([abs(x - cx) for x in range(width)])
    return np.add(xs, ys)


def process(data):
    left = min(x for x, y in data)
    right = max(x for x, y in data)
    top = min(y for x, y in data)
    bottom = max(y for x, y in data)
    data = [(x - left, y - top) for x, y in data]
    width, height = right - left, bottom - top

    distance_grids = np.array([distance_grid(loc, width, height) for loc in data])

    closest_locations = distance_grids.argmin(0)
    # Find locations of equal distance and replace with -1
    closest_locations[(distance_grids == distance_grids.min(0)).sum(0) > 1] = -1

    u, c = np.unique(closest_locations, return_counts=True)
    areas = dict(zip(u, c))

    on_edge = set(closest_locations[0, :])\
        .union(set(closest_locations[-1, :]))\
        .union(set(closest_locations[:, 0]))\
        .union(set(closest_locations[:, -1]))

    for i in on_edge:
        del areas[i]

    print(areas)
    print(max(areas.items(), key=lambda item: item[1]))


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    with open(args.file, 'r') as f:
        data = [location(s) for s in f]
        process(data)


if __name__ == '__main__':
    main()
