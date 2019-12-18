from argparse import ArgumentParser
import numpy as np
from intvm import IntVM


class Imager:
    SPACE = 0
    SCAFFOLD = 1

    def __init__(self, program):
        self.img_coord = 0, 0
        self.robot_coord = None
        self.program = program
        self.vm = IntVM(self.program, inputs=[], output_func=self.process_pixel)
        self.image = np.zeros((40, 51), dtype=int)
        self.map = ""

    def run(self):
        self.vm.run()

    def process_pixel(self, value):
        self.map = self.map + chr(value)
        x, y = self.img_coord
        if value == ord('\n'):
            x, y = 0, y + 1
        elif value == ord('.'):
            self.image[x, y] = self.SPACE
            x += 1
        elif value in (ord('#'), ord('<'), ord('^'), ord('>'), ord('v')):
            self.image[x, y] = self.SCAFFOLD
            self.robot_coord = x, y
            x += 1
        self.img_coord = x, y

    def get_answer(self):
        intersections = (self.image[1:-1, 1:-1] == self.SCAFFOLD) & \
                (self.image[0:-2, 1:-1] == self.SCAFFOLD) & \
                (self.image[2:, 1:-1] == self.SCAFFOLD) & \
                (self.image[1:-1, 0:-2] == self.SCAFFOLD) & \
                (self.image[1:-1, 2:] == self.SCAFFOLD)

        return sum((x+1) * (y+1) for x, y in np.argwhere(intersections))


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str, nargs="?", default="17-input.txt")
    args = argparse.parse_args()

    with open(args.file, "r") as f:
        program = [int(c) for c in f.read().split(',')]

    image = np.zeros((40, 50), dtype=int)

    imager = Imager(program)
    imager.run()

    print(imager.get_answer())
    with open("17-map.txt", "w") as f:
        f.write(imager.map)


if __name__ == '__main__':
    main()
