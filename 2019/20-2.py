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
                                self.entry = y + dy, x + dx, 0
                            elif name == "ZZ":
                                self.exit = y + dy, x + dx, 0
                            else:
                                self.map[y, x] = self.TILE_PORTAL
                                self.map[y-dy, x-dx] = self.TILE_EMPTY

                                self.portal_entries[c1 + c2].append((y, x))
                                self.portal_exits[c1 + c2].append((y + dy, x + dx))
                            break

        # Determine which portals go down (z+1) and which go up (z-1)
        h, w = self.map.shape
        cy, cx = h//2, w//2

        for name, ((y1, x1), (y2, x2)) in self.portal_entries.items():
            d1 = (y1-cy)**2+(x1-cx)**2
            d2 = (y2-cy)**2+(x2-cx)**2
            self.portals[y1, x1] = self.portal_exits[name][1], +1 if d1 < d2 else -1
            self.portals[y2, x2] = self.portal_exits[name][0], +1 if d1 > d2 else -1

    def find_path(self, current_loc, target_loc):
        not_traversed = 999999

        fill_map = defaultdict(lambda: not_traversed)
        fill_queue = [current_loc]
        fill_map[current_loc] = 0

        best_distance = not_traversed

        while fill_queue:
            sy, sx, sz = fill_queue.pop(0)
            dist = fill_map[sy, sx, sz] + 1
            if dist > best_distance:
                continue
            for dy, dx in ((-1, 0), (+1, 0), (0, -1), (0, +1)):
                y, x, z = sy + dy, sx + dx, sz

                if self.map[y, x] == self.TILE_PORTAL:
                    (ny, nx), dz = self.portals[y, x]
                    if z + dz >= 0:
                        y, x, z = ny, nx, z+dz
                    else:
                        continue

                if (y, x, z) == target_loc:
                    best_distance = dist

                if self.map[y, x] == self.TILE_EMPTY and fill_map[y, x, z] > dist:
                    fill_map[y, x, z] = dist
                    fill_queue.append((y, x, z))

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
