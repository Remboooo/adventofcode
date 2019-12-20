from argparse import ArgumentParser
import numpy as np
from intvm import IntVM


class Imager:
    def __init__(self, program):
        self.program = program

    def get_tractor_map(self):
        vm = IntVM(self.program)
        image = np.zeros((50, 50), dtype=int)

        for y in range(50):
            for x in range(50):
                def process_pixel(val):
                    image[y, x] = val
                vm.input_gen = iter([x, y])
                vm.output_func = process_pixel
                vm.run()

        return image


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str, nargs="?", default="19-input.txt")
    args = argparse.parse_args()

    with open(args.file, "r") as f:
        program = [int(c) for c in f.read().split(',')]

    imager = Imager(program)
    themap = imager.get_tractor_map()
    for line in themap:
        print(''.join('#' if t else ' ' for t in line))

    print(np.sum(themap == 1))


if __name__ == '__main__':
    main()
