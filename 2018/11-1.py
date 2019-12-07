from argparse import ArgumentParser
import numpy as np
from scipy.ndimage import convolve


def get_power_level(x, y, serial):
    rack_id = x + 10
    level = rack_id * y
    level += serial
    level *= rack_id
    level = (level // 100) % 10
    level -= 5
    return level


def process(data):
    serial = int(data)

    grid = np.zeros((301, 301), dtype=int)
    for x in range(1, 301):
        for y in range(1, 301):
            grid[x, y] = get_power_level(x, y, serial)

    np.set_printoptions(threshold=np.inf, linewidth=np.inf)
    print(grid[32:37, 44:49].T)

    total_powers = convolve(grid, np.ones((3, 3), dtype=int), mode='constant', cval=0, origin=(1, 1))
    max_x, max_y = np.unravel_index(total_powers.argmax(), total_powers.shape)
    print((max_x, max_y))


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    try:
        with open(args.file, 'r') as f:
                process(f.readline().strip())
    except FileNotFoundError:
        process(args.file)


if __name__ == '__main__':
    main()

