from argparse import ArgumentParser
import numpy as np


def read_layers(digits, w, h):
    layers = np.array([int(c) for c in digits]).reshape((len(digits) // (w*h), h, w))
    return np.swapaxes(layers, 1, 2)


def print_layer(layer):
    for y in range(layer.shape[1]):
        print(''.join(" " if p == 0 else "#" if p == 1 else "." for p in layer[:, y]))
    print()


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        digits = f.read().strip()

    w, h = 25, 6
    layers = read_layers(digits, w, h)

    image = np.ndarray((w, h), dtype=int)
    image.fill(2)

    for layer in layers:
        image[image == 2] = layer[image == 2]

    print_layer(image)


if __name__ == '__main__':
    main()
