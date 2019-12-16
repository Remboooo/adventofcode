from argparse import ArgumentParser
import numpy as np


class OxygenFiller:
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

    TILE_UNKNOWN = 0
    TILE_EMPTY = 1
    TILE_WALL = 2
    TILE_OXYGEN = 3

    TILES = [".", " ", "#", "O"]

    def __init__(self, map_lines):
        self.map = np.zeros((len(map_lines[0]), len(map_lines)), dtype=int)
        self.start_coord = None
        for y, line in enumerate(map_lines):
            for x, tile in enumerate(line):
                if tile == "X":
                    self.map[x, y] = self.TILE_EMPTY
                    self.start_coord = (x, y)
                elif tile == "O":
                    self.map[x, y] = self.TILE_OXYGEN
                    self.oxygen_coord = (x, y)
                else:
                    self.map[x, y] = self.TILES.index(tile)

    def fill(self):
        fill_map = np.ndarray(self.map.shape, dtype=int)
        fill_map.fill(999)
        fill_queue = [self.oxygen_coord]
        fill_map[self.oxygen_coord] = 0

        while fill_queue:
            sx, sy = fill_queue.pop(-1)
            dist = fill_map[sx, sy] + 1
            for dx, dy in ((-1, 0), (+1, 0), (0, -1), (0, +1)):
                x, y = sx + dx, sy + dy
                if self.map[x, y] == self.TILE_EMPTY and fill_map[x, y] > dist:
                    fill_map[x, y] = dist
                    fill_queue.append((x, y))

        mx, my = self.map.shape
        for y in range(my):
            print(' '.join("{:3d}".format(fill_map[x, y]) if self.map[x, y] == self.TILE_EMPTY
                           else self.TILES[self.map[x, y]] * 3
                           for x in range(mx)))

        return np.max(fill_map[fill_map != 999])


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str, nargs="?", default="15-map.txt")
    argparse.add_argument("--fps", "-f", type=int, nargs="?", default=10)
    args = argparse.parse_args()

    with open(args.file, "r") as f:
        map_lines = [l.strip() for l in f.readlines()]

    filler = OxygenFiller(map_lines)
    last_minute = filler.fill()
    print("Answer = {}".format(last_minute))


if __name__ == '__main__':
    main()
