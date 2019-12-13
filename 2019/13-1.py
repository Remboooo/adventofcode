from argparse import ArgumentParser
from intvm import IntVM, MultiOutput
import numpy as np


class Arcade:
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4
    TILES = (" ", "█", "▒", "━", "●")

    def __init__(self, program, screen_w=37, screen_h=20):
        self.screen = np.zeros((screen_w, screen_h), dtype=int)
        self.program = program
        self.vm = IntVM(program, inputs=[], output_func=MultiOutput(self._draw, 3))

    def _draw(self, x, y, tile):
        self.screen[x, y] = tile

    def run(self):
        self.vm.run()

    def draw_screen(self):
        for row in self.screen.T:
            print(''.join(self.TILES[t] if 0 <= t < len(self.TILES) else "?" for t in row))


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()

    with open(args.file, "r") as f:
        program = [int(c) for c in f.read().split(',')]

    arcade = Arcade(program)
    arcade.run()
    arcade.draw_screen()

    print(np.sum(arcade.screen == Arcade.BLOCK))


if __name__ == '__main__':
    main()
