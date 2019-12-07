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

    distance_sums = distance_grids.sum(0)
    print((distance_sums < 10000).sum())


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    with open(args.file, 'r') as f:
        data = [location(s) for s in f]
        process(data)


if __name__ == '__main__':
    main()
