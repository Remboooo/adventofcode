import sys
from argparse import ArgumentParser
from collections import defaultdict

import numpy as np


class Finder:
    TILE_EMPTY = '.'
    TILE_WALL = '#'
    TILE_PORTAL = '@'

    def __init__(self, map):
        self.map = map
        self.entry = None
        self.exit = None

        self.portal_entries = defaultdict(list)
        self.portal_exits = defaultdict(list)
        self.portals = {}
        self.locate_portals()

    def locate_portals(self):
        for y, line in enumerate(self.map):
            for x, tile in enumerate(line):
                if 'A' <= tile <= 'Z':
                    for dy, dx in ((+1, 0), (-1, 0), (0, +1), (0, -1)):
                        if self.map[y+dy, x+dx] == self.TILE_EMPTY:
                            c1 = self.map[y, x]
                            c2 = self.map[y-dy, x-dx]
                            if dy > 0 or dx > 0:
                                c1, c2 = c2, c1

                            name = c1+c2
                            if name == "AA":
                                self.entry = y + dy, x + dx
                            elif name == "ZZ":
                                self.exit = y + dy, x + dx
                            else:
                                self.map[y, x] = self.TILE_PORTAL
                                self.map[y-dy, x-dx] = self.TILE_EMPTY

                                self.portal_entries[c1 + c2].append((y, x))
                                self.portal_exits[c1 + c2].append((y + dy, x + dx))
                            break

        for name, ((y1, x1), (y2, x2)) in self.portal_entries.items():
            self.portals[y1, x1] = self.portal_exits[name][1]
            self.portals[y2, x2] = self.portal_exits[name][0]

    def find_path(self, current_loc, target_loc):
        not_traversed = 999999

        fill_map = np.ndarray(self.map.shape, dtype=int)
        fill_map.fill(not_traversed)
        fill_queue = [current_loc]
        fill_map[current_loc] = 0

        best_distance = not_traversed

        while fill_queue:
            sy, sx = fill_queue.pop(-1)
            dist = fill_map[sy, sx] + 1
            if dist > best_distance:
                continue
            for dy, dx in ((-1, 0), (+1, 0), (0, -1), (0, +1)):
                y, x = sy + dy, sx + dx
                if self.map[y, x] == self.TILE_PORTAL:
                    y, x = self.portals[y, x]

                if (y, x) == target_loc:
                    best_distance = dist

                if self.map[y, x] == self.TILE_EMPTY and fill_map[y, x] > dist:
                    fill_map[y, x] = dist
                    fill_queue.append((y, x))
        """
        for y, l in enumerate(self.map):
            print(''.join(
                t*4 if fill_map[y, x] == not_traversed
                else "{: ^4d}".format(fill_map[y, x])
                for x, t in enumerate(l)
            ))
        """
        return best_distance

    def solve_maze(self):
        return self.find_path(self.entry, self.exit)

    def print_map(self):
        for l in self.map:
            print(''.join(t for t in l))


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str, nargs="?", default="20-input.txt")
    args = argparse.parse_args()

    with open(args.file, "r") as f:
        lines = [[]] + [[c for c in " " + l.strip('\r\n') + " "] for l in f.readlines()] + [[]]
        width = max(len(l) for l in lines)
        lines = [l + [' '] * (width - len(l)) for l in lines]
        themap = np.array(lines)

    finder = Finder(themap)
    print(finder.solve_maze())


if __name__ == '__main__':
    main()
