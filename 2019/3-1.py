from argparse import ArgumentParser


def read_coords(s):
    x = 0
    y = 0
    for movement in s.split(','):
        if movement[0] == 'U':
            dx = 0
            dy = -1
        elif movement[0] == 'D':
            dx = 0
            dy = +1
        elif movement[0] == 'R':
            dx = +1
            dy = 0
        elif movement[0] == 'L':
            dx = -1
            dy = 0
        else:
            raise ValueError(movement[0])

        for i in range(int(movement[1:])):
            x += dx
            y += dy
            yield (x, y)


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        coords1 = set(read_coords(f.readline()))
        coords2 = set(read_coords(f.readline()))
        crossings = coords1.intersection(coords2)
        print(min(abs(x) + abs(y) for x, y in crossings))


if __name__ == '__main__':
    main()
