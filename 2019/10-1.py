from argparse import ArgumentParser
import math


def get_visibles(cx, cy, asteroids):
    result = 0
    for x, y in sorted(asteroids):
        if (x, y) == (cx, cy):
            continue

        dx, dy = x - cx, y - cy
        gcd = math.gcd(dx, dy)
        sdx, sdy = dx // gcd, dy // gcd

        if dx == 0 and any(ax == x and (y < ay < cy or y > ay > cy) for ax, ay in asteroids):
            continue  # Horizontally blocked
        elif dy == 0 and any(ay == y and (x < ax < cx or x > ax > cx) for ax, ay in asteroids):
            continue  # Vertically blocked
        elif gcd > 1 and any((cx + m * sdx, cy + m * sdy) in asteroids for m in range(1, gcd)):
            continue  # Diagonally blocked

        result += 1
    return result


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        grid = [[char == '#' for char in line.strip()] for line in f.readlines()]

    asteroids = set((x, y) for y, line in enumerate(grid) for x, pos in enumerate(line) if pos)

    max_visibles = 0
    best_pos = None

    for x, y in sorted(asteroids):
        visibles = get_visibles(x, y, asteroids)
        if visibles > max_visibles:
            max_visibles = visibles
            best_pos = (x, y)

    print("{}: {}".format(best_pos, max_visibles))


if __name__ == '__main__':
    main()
