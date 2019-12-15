import curses
import sys
import time
from argparse import ArgumentParser

import numpy as np

from intvm import IntVM
from curses import wrapper


class OxygenFinder:
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

    deltas = {
        NORTH: (0, -1),
        SOUTH: (0, +1),
        WEST: (-1, 0),
        EAST: (+1, 0),
    }

    STATUS_WALL = 0
    STATUS_MOVED = 1
    STATUS_FOUND_OXYGEN = 2

    TILE_UNKNOWN = 0
    TILE_EMPTY = 1
    TILE_WALL = 2
    TILE_OXYGEN = 3

    TILES = ["▒", " ", "█", "O"]

    def __init__(self, program, fps=10):
        self.map = np.zeros((1000, 1000), dtype=int)
        self.current_coord = 500, 500
        self.initial_coord = self.current_coord
        self.oxygen_coord = None
        self.map[self.current_coord] = self.TILE_EMPTY
        self.current_direction = self.WEST
        self.explore_queue = []
        x, y = self.current_coord
        self.min_x, self.min_y, self.max_x, self.max_y = x, y, x, y
        self.queue_surrounding_tiles()
        self.curses_window = None

        self.last_screen = 0
        self.screen_interval = 1 / fps if fps > 0 else 0

        self.program = program
        self.vm = IntVM(self.program, inputs=self, output_func=self.process_output)

    def __iter__(self):
        return iter(self.get_input, -1)

    def find_path(self, start, to):
        dist_map = np.zeros(self.map.shape, dtype=int)
        dist_map.fill(10000000)

        dist_map[to] = 0
        stack = [to]

        while stack:
            x, y = stack.pop(-1)
            if (x, y) == start:
                break
            current_dist = dist_map[x, y] + 1

            for candidate in (x-1, y), (x+1, y), (x, y-1), (x, y+1):
                if self.map[candidate] != self.TILE_WALL and \
                        (self.map[candidate] != self.TILE_UNKNOWN or self.map[x, y] != self.TILE_UNKNOWN) \
                        and current_dist < dist_map[candidate]:
                    stack.append(candidate)
                    dist_map[candidate] = current_dist

        min_dist = 100000
        min_direction = None
        x, y = start
        for direction, (dx, dy) in self.deltas.items():
            candidate = (x+dx, y+dy)
            if dist_map[candidate] < min_dist:
                min_dist = dist_map[candidate]
                min_direction = direction

        return min_direction, min_dist

    def get_input(self):
        direction, _ = self.find_path(self.current_coord, self.explore_queue[-1])
        self.current_direction = direction
        return direction

    def get_next_coord(self, direction=None):
        direction = self.current_direction if direction is None else direction
        x, y = self.current_coord
        dx, dy = self.deltas[direction]
        return x + dx, y + dy

    def queue_surrounding_tiles(self):
        for direction in (self.NORTH, self.EAST, self.WEST, self.SOUTH):
            nx, ny = self.get_next_coord(direction)
            if self.map[nx, ny] == self.TILE_UNKNOWN and (nx, ny) not in self.explore_queue:
                self.explore_queue.append((nx, ny))

    def process_output(self, value):
        # Process a robot status code
        if value == self.STATUS_WALL:
            wall_coord = self.get_next_coord()
            self.map[wall_coord] = self.TILE_WALL
            try:
                self.explore_queue.remove(wall_coord)
            except ValueError:
                pass
        elif value == self.STATUS_MOVED:
            self.current_coord = self.get_next_coord()
            self.map[self.current_coord] = self.TILE_EMPTY
            try:
                self.explore_queue.remove(self.current_coord)
            except ValueError:
                pass
            self.queue_surrounding_tiles()
        elif value == self.STATUS_FOUND_OXYGEN:
            self.current_coord = self.get_next_coord()
            self.map[self.current_coord] = self.TILE_OXYGEN
            self.oxygen_coord = self.current_coord

        x, y = self.current_coord
        self.min_x = min(self.min_x, x)
        self.min_y = min(self.min_y, y)
        self.max_x = max(self.max_x, x)
        self.max_y = max(self.max_y, y)

        self.frame()

    def draw_map(self):
        sx, sy = self.min_x - 1, self.min_y - 1
        my, mx = self.curses_window.getmaxyx()

        for y in range(self.min_y-1, self.max_y+2):
            for x in range(self.min_x-1, self.max_x+2):
                if y - sy < my and x - sx < mx:
                    self.curses_window.addch(y - sy, x - sx, ord(self.TILES[self.map[x, y]]))

        x, y = self.current_coord
        if y - sy < my and x - sx < mx and self.current_direction:
            self.curses_window.addch(y - sy, x - sx, ord(["^", "v", "<", ">"][self.current_direction - 1]))

        x, y = self.initial_coord
        if y - sy < my and x - sx < mx:
            self.curses_window.addch(y - sy, x - sx, ord("X"))

    def frame(self):
        if self.curses_window.getch() == 3:
            sys.exit(0)

        if self.screen_interval != 0:
            now = time.monotonic()
            if now - self.last_screen < self.screen_interval:
                time.sleep(self.screen_interval - (now - self.last_screen))

        self.draw_map()
        self.curses_window.refresh()

    def run_curses(self, stdscr):
        self.curses_window = stdscr
        self.curses_window.nodelay(1)
        curses.curs_set(0)
        self.vm.run()
        self.draw_map()
        self.curses_window.nodelay(0)
        _, oxygen_distance = self.find_path(self.initial_coord, self.oxygen_coord)
        self.curses_window.addstr(0, 0, "Distance {} -> {} = {}".format(self.initial_coord, self.oxygen_coord, oxygen_distance))
        self.curses_window.refresh()
        self.curses_window.getkey()


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str, nargs="?", default="15-input.txt")
    args = argparse.parse_args()

    with open(args.file, "r") as f:
        program = [int(c) for c in f.read().split(',')]

    finder = OxygenFinder(program)
    wrapper(finder.run_curses)


if __name__ == '__main__':
    main()
