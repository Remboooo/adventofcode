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

    best_square_size = None
    best_value = None
    best_coords = None

    for square_size in range(1, 301):
        total_powers = convolve(grid, np.ones((square_size, square_size), dtype=int), mode='constant', cval=0,
                                origin=((square_size-1)//2, (square_size-1)//2))
        max_x, max_y = np.unravel_index(total_powers.argmax(), total_powers.shape)
        value = total_powers[max_x, max_y]
        print("{}: {}, {} = {}".format(square_size, max_x, max_y, value))

        if best_value is None or value > best_value:
            best_value = value
            best_square_size = square_size
            best_coords = max_x, max_y
            print("Best: {},{},{}".format(best_coords[0], best_coords[1], best_square_size))

    print("Best: {},{},{}".format(best_coords[0], best_coords[1], best_square_size))


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

