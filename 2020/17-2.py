from argparse import ArgumentParser
import numpy as np
from scipy.ndimage import convolve

from util import timed

NEIGHBOURS = np.ones((3, 3, 3, 3), dtype=np.uint8)
NEIGHBOURS[1, 1, 1, 1] = 0


def parse_initial_state(f):
    state = np.array([[[[c == '#' for c in line.strip()] for line in f]]], dtype=np.uint8)
    state = np.moveaxis(state, (0, 1, 2, 3), (3, 2, 1, 0))  # Reorder dimensions to x, y, z, w
    return state


@timed
def run_cycles(state, n):
    for cycle in range(n):
        padded = np.pad(state, 1)
        neighbour_sums = convolve(padded, weights=NEIGHBOURS, mode='constant', cval=0)
        state = np.array(np.logical_or(neighbour_sums == 3, np.logical_and(padded == 1, neighbour_sums == 2)), dtype=np.uint8)
        yield state


def print_state(state):
    for iw, w in enumerate(range(-(state.shape[3] // 2), state.shape[3] // 2 + 1)):
        for iz, z in enumerate(range(-(state.shape[2] // 2), state.shape[2] // 2 + 1)):
            print(f"z={z}, w={w}")
            for iy in range(state.shape[1]):
                print(''.join('#' if state[ix, iy, iz, iw] else '.' for ix in range(state.shape[0])))
            print()


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="17-input.txt")
    argparse.add_argument("-n", nargs='?', type=int, default="6", help="Number of cycles to simulate")
    argparse.add_argument("--verbose", "-v", action='store_true', help="Output intermediate results")
    args = argparse.parse_args()

    with open(args.file, 'r') as f:
        state = parse_initial_state(f)

    if args.verbose:
        print("Start state:")
        print_state(state)

    end_state = []

    for cycle, state in enumerate(run_cycles(state, args.n), 1):
        end_state = state
        if args.verbose:
            print(f"=== CYCLE {cycle} ===")
            print_state(state)

    print(np.sum(end_state))


if __name__ == '__main__':
    main()
