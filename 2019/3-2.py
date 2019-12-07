from argparse import ArgumentParser


def read_coords(string):
    x = 0
    y = 0
    s = 0
    for movement in string.split(','):
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
            s += 1
            yield (x, y, s)


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        steps1 = {(x, y): s for x, y, s in read_coords(f.readline())}
        steps2 = {(x, y): s for x, y, s in read_coords(f.readline())}

        crossings = set(steps1.keys()).intersection(set(steps2.keys()))

        print(min(steps1[crossing] + steps2[crossing] for crossing in crossings))


if __name__ == '__main__':
    main()
