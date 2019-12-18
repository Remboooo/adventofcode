from argparse import ArgumentParser
import numpy as np
from intvm import IntVM


class Imager:
    SPACE = 0
    SCAFFOLD = 1

    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    deltas = [(0, -1), (1, 0), (0, 1), (-1, 0)]
    directions = {'<': WEST, '>': EAST, '^': NORTH, 'v': SOUTH}

    def __init__(self, program):
        self.img_coord = 0, 0
        self.robot_coord = None
        self.robot_direction = None
        self.program = program
        self.input = []
        self.vm = IntVM(self.program, inputs=self.input, output_func=self.process_pixel)
        self.image = np.zeros((40, 51), dtype=int)
        self.raw_map = ""
        self.map = None

    def get_initial_image(self):
        self.vm.program[0] = 1
        self.vm.output_func = self.process_pixel
        self.vm.run()
        w, h = self.image.shape
        # Add zeroes to the edge of the map to avoid peppering everything with boundary checks
        self.map = np.zeros((w+2, h+2), dtype=int)
        self.map[1:-1, 1:-1] = self.image
        self.robot_coord = self.robot_coord[0] + 1, self.robot_coord[1] + 1

    def process_pixel(self, raw_value):
        x, y = self.img_coord
        value = chr(raw_value)
        self.raw_map = self.raw_map + value
        if value == '\n':
            x, y = 0, y + 1
        elif value == '.':
            self.image[x, y] = self.SPACE
            x += 1
        elif value in ('#', '<', '^', '>', 'v'):
            self.image[x, y] = self.SCAFFOLD
            if value in self.directions:
                self.robot_coord = x, y
                self.robot_direction = self.directions[value]
            x += 1
        self.img_coord = x, y

    def get_desired_route(self):
        at_end = False
        x, y = self.robot_coord
        direction = self.robot_direction
        while not at_end:
            dx, dy = self.deltas[direction]
            if self.map[x + dx, y + dy] == self.SCAFFOLD:
                x += dx
                y += dy
                yield '1'
            else:
                rdx, rdy = self.deltas[(direction + 1) % 4]
                ldx, ldy = self.deltas[(direction - 1) % 4]
                if self.map[x + rdx, y + rdy] == self.SCAFFOLD:
                    direction = (direction + 1) % 4
                    yield 'R'
                elif self.map[x + ldx, y + ldy] == self.SCAFFOLD:
                    direction = (direction - 1) % 4
                    yield 'L'
                else:
                    at_end = True

    def route_output(self, value):
        if value > 128:
            print("Answer: {}".format(value))

    def run_route(self, main_func, a_func, b_func, c_func):
        self.vm.program[0] = 2
        self.vm.output_func = self.route_output
        config_str = "\n".join([main_func, a_func, b_func, c_func, "n", ""])
        self.vm.input_gen = iter(ord(c) for c in config_str)
        self.vm.run()


def compress(route, compressed=None, dictionary=None):
    if dictionary is None:
        dictionary = []

    if compressed is None:
        compressed = []

    if not route:
        # We have no route left, so we've compressed everything
        yield compressed, [compress_forwards(d) for d in dictionary]

    for k, v in enumerate(dictionary):
        # Try to match the first part of the (remaining) route to an item in the dictionary
        if len(v) <= len(route) and route[:len(v)] == v:
            yield from compress(route[len(v):], compressed + [k], dictionary)

    if len(dictionary) < 3:
        # Create a new item in the dictionary containing an arbitrary chunk from the start of the remaining route
        for chunk_size in range(4, len(route)):
            k = len(dictionary)
            yield from compress(route[chunk_size:], compressed + [k], dictionary + [route[:chunk_size]])


def compress_forwards(route):
    result = []
    length = 0
    for r in route:
        if r in ("L", "R"):
            if length > 0:
                result.append(str(length))
                length = 0
            result.append(r)
        elif r == "1":
            length += 1
    if length > 0:
        result.append(str(length))

    return result


def main():
    argparse = ArgumentParser()
    argparse.add_argument("program", type=str, nargs="?", default="17-input.txt")
    args = argparse.parse_args()

    with open(args.program, "r") as f:
        program = [int(c) for c in f.read().split(',')]

    image = np.zeros((40, 50), dtype=int)

    imager = Imager(program)
    imager.get_initial_image()

    route = list(imager.get_desired_route())
    print("Found route: {}".format(",".join(compress_forwards(route))))

    print("Compressing route...")
    main_def, func_defs = None, []
    for main_routine, functions in compress(route):
        main_def = ",".join(["A", "B", "C"][f] for f in main_routine)
        func_defs = [",".join(func) for func in functions]
        if all(len(f) <= 20 for f in func_defs) and len(main_def) <= 20:
            print()
            print("Main: " + main_def)
            for f in func_defs:
                print(f)
            break

    if not main_def or not func_defs:
        print("No route found")
        return

    imager.run_route(main_def, *func_defs)


if __name__ == '__main__':
    main()
