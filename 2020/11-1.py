from argparse import ArgumentParser

from util import timed


def evolve(seat_map):
    new_seat_map = [row.copy() for row in seat_map]
    for nrow, row in enumerate(seat_map[1:-1], 1):
        for ncol, seat in enumerate(row[1:-1], 1):
            occupancy = sum(seat_map[nrow+dy][ncol+dx] == '#' for dx, dy in (
                (-1, -1), ( 0, -1), (+1, -1),
                (-1,  0),           (+1,  0),
                (-1, +1), ( 0, +1), (+1, +1),
            ))
            if occupancy == 0 and seat_map[nrow][ncol] == 'L':
                new_seat_map[nrow][ncol] = '#'
            if occupancy >= 4 and seat_map[nrow][ncol] == '#':
                new_seat_map[nrow][ncol] = 'L'

    return new_seat_map


@timed
def evolve_until_stable(seat_map):
    # Pad seat map so we don't have to special-case the edges in array indexing
    seat_map = [[' '] + row + [' '] for row in seat_map]
    seat_map = [[' '] * len(seat_map[0])] + seat_map + [[' '] * len(seat_map[0])]

    while True:
        new_seat_map = evolve(seat_map)
        if new_seat_map == seat_map:
            break
        else:
            seat_map = new_seat_map
        #print('\n'.join([''.join(row) for row in seat_map]))

    return new_seat_map


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="11-input.txt")
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        seat_map = [list(stripped) for stripped in (line.strip() for line in f) if stripped]
        final_seating = evolve_until_stable(seat_map)

    print('\n'.join([''.join(row) for row in final_seating]))
    print(sum(1 if c == '#' else 0 for row in final_seating for c in row))


if __name__ == '__main__':
    main()
