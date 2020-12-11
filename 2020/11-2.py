from argparse import ArgumentParser

from util import timed


def find_visible_seats(seat_map):
    def find_visible_seats_from(nrow, ncol):
        for dx, dy in (
                (-1, -1), (0, -1), (+1, -1),
                (-1,  0),          (+1,  0),
                (-1, +1), (0, +1), (+1, +1),
        ):
            x = ncol + dx
            y = nrow + dy
            while 0 <= x < len(seat_map[0]) and 0 <= y < len(seat_map):
                if seat_map[y][x] in ('#', 'L'):
                    yield x, y
                    break
                x += dx
                y += dy

    return [
        [list(find_visible_seats_from(nrow, ncol)) for ncol, _ in enumerate(row)]
        for nrow, row in enumerate(seat_map)
    ]


def evolve(seat_map, visible_seats):
    new_seat_map = [row.copy() for row in seat_map]
    for nrow, row in enumerate(seat_map):
        for ncol, seat in enumerate(row):
            occupancy = sum(seat_map[y][x] == '#' for x, y in visible_seats[nrow][ncol])
            if occupancy == 0 and seat_map[nrow][ncol] == 'L':
                new_seat_map[nrow][ncol] = '#'
            if occupancy >= 5 and seat_map[nrow][ncol] == '#':
                new_seat_map[nrow][ncol] = 'L'

    return new_seat_map


@timed
def evolve_until_stable(seat_map):
    visible_seats = find_visible_seats(seat_map)

    while True:
        new_seat_map = evolve(seat_map, visible_seats)
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
