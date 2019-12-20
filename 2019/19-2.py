from argparse import ArgumentParser
import numpy as np
from intvm import IntVM


class Imager:
    def __init__(self, program):
        self.program = program
        self.pixel_cache = {}
        self.vm = IntVM(self.program)

    def beam_at(self, y, x):
        try:
            return self.pixel_cache[(y, x)]
        except KeyError:
            def process_pixel(val):
                self.pixel_cache[(y, x)] = val

            self.vm.input_gen = iter((x, y))
            self.vm.output_func = process_pixel
            self.vm.run()
            return self.pixel_cache[(y, x)]

    def find_left(self, y, x):
        # Assumes x to be to the left of the starting pixel
        while not self.beam_at(y, x):
            x += 1
        # Returns first pixel inside beam
        return x

    def find_right(self, y, x):
        # Assumes x to be to the left of, or inside the beam
        while not self.beam_at(y, x):
            x += 1
        while self.beam_at(y, x):
            x += 1
        # Returns last pixel inside beam
        return x - 1

    def find_square(self, size=100):
        # Top right edge
        ty, tx = 10, 0
        # Bottom left edge
        by, bx = 10+size-1, 0

        tx = self.find_right(ty, tx)
        bx = self.find_left(by, bx)

        while tx - bx < size-1:
            ty += 1
            by += 1
            tx = self.find_right(ty, tx)
            bx = self.find_left(by, bx)

            print("Width of rectangle of height {} at y={}: {}..{}={}".format(size, ty, bx, tx, tx-bx+1))

        return (ty, tx), (by, bx)

    def get_map(self, miny, maxy, minx, maxx):
        return np.array([[self.beam_at(y, x) for x in range(minx, maxx)] for y in range(miny, maxy)], dtype=int)


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str, nargs="?", default="19-input.txt")
    args = argparse.parse_args()

    with open(args.file, "r") as f:
        program = [int(c) for c in f.read().split(',')]

    imager = Imager(program)
    (ty, tx), (by, bx) = imager.find_square()

    print("Top right {}, bottom left {}".format((tx, ty), (bx, by)))
    print("Answer: {}".format(bx * 10000 + ty))


if __name__ == '__main__':
    main()
