import sys
from argparse import ArgumentParser

import numpy as np


class ShortestPathHolder:
    def __init__(self):
        self.shortest_path_sequence = []
        self.shortest_path_length = 100000


class Finder:
    TILE_EMPTY = '.'
    TILE_WALL = '#'

    def __init__(self, map, shortest_path_holder=None, keys=None, reverse_keys=None, doors=None):
        self.map = map
        self.doors = doors if doors is not None else {}
        self.keys = keys if keys is not None else {}
        self.entrance = None
        if keys is None or doors is None:
            self.locate_objects()
        self.reverse_keys = reverse_keys if reverse_keys is not None else {l: k for k, l in self.keys.items()}
        self.current_loc = self.entrance
        self.steps_done = 0
        self.key_sequence = []
        self.shortest_path_holder = shortest_path_holder if shortest_path_holder is not None else ShortestPathHolder()
        self.distance_cache = {}

    def locate_objects(self):
        for y, line in enumerate(self.map):
            for x, tile in enumerate(line):
                if 'a' <= tile <= 'z':
                    self.keys[str(tile)] = (y, x)
                    self.map[y, x] = self.TILE_EMPTY
                elif 'A' <= tile <= 'Z':
                    self.doors[str(tile)] = (y, x)
                    self.map[y, x] = self.TILE_EMPTY
                elif tile == '@':
                    self.entrance = (y, x)
                    self.map[y, x] = self.TILE_EMPTY

    def _get_reachable_keys_steps(self, current_loc, keys, doors, reverse_keys):
        fill_map = np.ndarray(self.map.shape, dtype=int)
        fill_map.fill(999)
        fill_queue = [current_loc]
        fill_map[current_loc] = 0

        reachable_keys = {}

        for y, x in keys.values():
            fill_map[y, x] = -1

        for y, x in doors.values():
            fill_map[y, x] = -1

        while fill_queue:
            sy, sx = fill_queue.pop(-1)
            dist = fill_map[sy, sx] + 1
            for dx, dy in ((-1, 0), (+1, 0), (0, -1), (0, +1)):
                x, y = sx + dx, sy + dy
                if (y, x) in reverse_keys:
                    reachable_keys[reverse_keys[(y, x)]] = dist
                elif self.map[y, x] == self.TILE_EMPTY and fill_map[y, x] > dist:
                    fill_map[y, x] = dist
                    fill_queue.append((y, x))

        return reachable_keys

    def print_map(self):
        for l in self.map:
            print(''.join(t for t in l))

    def _shortest_path_all_keys_it(self, current_coord, keys, rev_keys, doors):
        cache_key = (current_coord, frozenset(keys.keys()))
        try:
            return self.distance_cache[cache_key]
        except KeyError:
            pass

        min_steps, min_sequence = None, None
        for key, key_steps in self._get_reachable_keys_steps(current_coord, keys, doors, rev_keys).items():
            if len(keys) == 1:
                # Last key; no use copying the map etc, we already know the total path length
                min_steps, min_sequence = key_steps, [key]
            else:
                if min_steps is not None and key_steps >= min_steps:
                    continue

                # Probably more efficient to pass a list of keys to ignore rather than copying all of this, but w/e...
                new_keys = keys.copy()
                new_reverse_keys = rev_keys.copy()
                new_doors = doors.copy()
                door = key.upper()
                if door in doors:
                    del new_doors[door]
                del new_keys[key]
                del new_reverse_keys[keys[key]]

                key_min_steps, key_min_sequence = self._shortest_path_all_keys_it(keys[key], new_keys, new_reverse_keys, new_doors)
                if key_min_steps is not None:
                    if min_steps is None or key_steps + key_min_steps < min_steps:
                        min_steps, min_sequence = key_steps + key_min_steps, [key] + key_min_sequence

        self.distance_cache[cache_key] = min_steps, min_sequence
        return min_steps, min_sequence

    def get_shortest_path_all_keys(self):
        return self._shortest_path_all_keys_it(self.entrance, self.keys, self.reverse_keys, self.doors)


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str, nargs="?", default="18-input.txt")
    args = argparse.parse_args()

    with open(args.file, "r") as f:
        themap = np.array([[c for c in l.strip()] for l in f.readlines()])

    finder = Finder(themap)

    key_sequence, sequence_steps = finder.get_shortest_path_all_keys()
    print(key_sequence)
    print(sequence_steps)


if __name__ == '__main__':
    main()
