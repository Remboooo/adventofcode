from itertools import count

from argparse import ArgumentParser


class Unit:
    def __init__(self, location, type):
        self.hp = 200
        self.attack = 3
        self.location = location
        self.type = type


def read_input(data):
    walls = [[c == '#' for c in line] for line in data]
    units = []
    for y, row in enumerate(data):
        for x, c in enumerate(row):
            if c not in '#.':
                units.append(Unit((y, x), c))
    return walls, units


def print_state(walls, units):
    chars = [["#" if p else "." for p in row] for row in walls]
    for unit in units:
        y, x = unit.location
        chars[y][x] = unit.type
    print("\n".join("".join(row) for row in chars))


def distance(location, target, obstacles):
    distances = [[None for _ in row] for row in obstacles]
    ly, lx = location

    ty, tx = target
    distances[ty][tx] = 0
    original_obstacle = obstacles[ly][lx]
    obstacles[ly][lx] = False

    changed = True
    while changed and distances[ly][lx] is None:
        changed = False
        for y, row in enumerate(obstacles):
            for x, obstacle in enumerate(row):
                if not obstacle and distances[y][x] is None:
                    for dy, dx in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
                        if distances[y + dy][x + dx] is not None:
                            distances[y][x] = distances[y + dy][x + dx] + 1
                            changed = True

    obstacles[ly][lx] = original_obstacle
    return distances[ly][lx], distances


def get_obstacles(units, walls):
    obstacles = [[p for p in row] for row in walls]
    for u in units:
        y, x = u.location
        obstacles[y][x] = True
    return obstacles


def process(data):
    walls, units = read_input(data)

    for iteration in count():
        print("Iteration {}".format(iteration))
        obstacles = get_obstacles(units, walls)

        print_state(walls, units)

        units = sorted(units, key=lambda u: u.location)

        for unit in units:
            target_squares = []

            for target in units:
                if unit.type == target.type:
                    continue
                ty, tx = target.location

                for dy, dx in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
                    y, x = ty + dy, tx + dx
                    if unit.location == (y, x) or not obstacles[y][x]:
                        target_squares.append((y, x))

            if unit.location not in target_squares:
                # Move
                distances = [(distance(unit.location, target_square, obstacles), target_square)
                             for target_square in target_squares]

                distances = sorted([(d, target, distance_map) for (d, distance_map), target in distances
                                    if d is not None])

                if not distances:
                    print("No reachable enemies left")
                    return

                print([(d, target) for d, target, *_ in distances])
                target_distance, target, distance_map = distances[0]
                print("Target for {} at {} is {} at distance {}".format(unit.type, unit.location, target,
                                                                        target_distance))
                y, x = unit.location

                print(sorted((distance_map[y + dy][x + dx], y + dy, x + dx)
                                                             for dy, dx in [(-1, 0), (+1, 0), (0, -1), (0, +1)]
                                                             if distance_map[y + dy][x + dx] is not None))

                min_distance, min_coord_y, min_coord_x = min((distance_map[y + dy][x + dx], y + dy, x + dx)
                                                             for dy, dx in [(-1, 0), (+1, 0), (0, -1), (0, +1)]
                                                             if distance_map[y + dy][x + dx] is not None)

                print(" => moving to {},{}".format(min_coord_x, min_coord_y))
                unit.location = (min_coord_y, min_coord_x)

            if unit.location in target_squares:
                # Attack
                print("ATTTAAAAACK")
                pass

        print()
        if iteration > 10:
            break


if __name__ == '__main__':
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    with open(args.file, 'r') as f:
        process([l.rstrip('\r\n') for l in f])
