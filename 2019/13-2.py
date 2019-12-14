import curses
import sys
import time
from argparse import ArgumentParser
from intvm import IntVM, MultiOutput
import numpy as np
from curses import wrapper


class Arcade:
    EMPTY = 0
    WALL = 1
    BLOCK = 2
    PADDLE = 3
    BALL = 4

    TILES = (" ", "█", "▒", "═", "o")

    JOY_LEFT = -1
    JOY_MIDDLE = 0
    JOY_RIGHT = 1

    def __init__(self, program, quarters=2, fps=10):
        self.program = program.copy()
        self.program[0] = quarters
        self.vm = IntVM(self.program, inputs=self, output_func=MultiOutput(self._output, 3))
        self.score = 0
        self.paddle_x = 0
        self.joystick_position = self.JOY_MIDDLE
        self.scr = None
        self.last_screen = 0
        self.screen_interval = 1 / fps if fps > 0 else 0

    def __iter__(self):
        return iter(lambda: self.joystick_position, -2)

    def _output(self, x, y, tile):
        if (x, y) == (-1, 0):
            self.score = tile
        else:
            self.scr.addstr(y, x, self.TILES[tile] if 0 <= tile < len(self.TILES) else "?")

            if tile == self.BALL:
                self.ball_x = x
                self.adjust_joystick()
            elif tile == self.PADDLE:
                self.paddle_x = x
                self.adjust_joystick()
                self.draw_screen()

    def adjust_joystick(self):
        if self.ball_x < self.paddle_x:
            self.joystick_position = self.JOY_LEFT
        elif self.ball_x > self.paddle_x:
            self.joystick_position = self.JOY_RIGHT
        else:
            self.joystick_position = self.JOY_MIDDLE

    def run(self, stdscr):
        self.scr = stdscr
        self.scr.nodelay(1)
        curses.curs_set(0)
        self.vm.run()
        self.scr.nodelay(0)
        self.scr.addstr(23, 0, "Score: {}, GAME OVER - press key to exit".format(self.score))
        self.scr.refresh()
        self.scr.getkey()

    def draw_screen(self):
        if self.scr.getch() == 3:
            sys.exit(0)

        if self.screen_interval != 0:
            now = time.monotonic()
            if now - self.last_screen < self.screen_interval:
                time.sleep(self.screen_interval - (now - self.last_screen))

        self.scr.addstr(23, 0, "Score: {}".format(self.score))
        self.scr.refresh()
        self.last_screen = time.monotonic()


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str, nargs="?", default="13-input.txt")
    argparse.add_argument("--fps", "-f", type=int, nargs="?", default=0)
    args = argparse.parse_args()

    with open(args.file, "r") as f:
        program = [int(c) for c in f.read().split(',')]

    arcade = Arcade(program)
    wrapper(arcade.run)


if __name__ == '__main__':
    main()
