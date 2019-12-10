from argparse import ArgumentParser
import math


def get_visibles(cx, cy, asteroids):
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

        yield (x, y)


def get_rel_angle(center, asteroid, rot):
    cx, cy = center
    ax, ay = asteroid

    dx, dy = ax - cx, ay - cy

    angle = math.atan2(dx, -dy)  # 0 is at the top, +pi/2 is right

    rel_angle = angle - rot
    while rel_angle <= 0:
        rel_angle += 2 * math.pi

    return rel_angle


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    argparse.add_argument("loc", type=str, nargs="?", default="23,19")
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        grid = [[char == '#' for char in line.strip()] for line in f.readlines()]

    asteroids = set((x, y) for y, line in enumerate(grid) for x, pos in enumerate(line) if pos)

    cx, cy = (int(s) for s in args.loc.split(","))
    rot = -1e-9  # Slightly before 0 because the relative angle to the next asteroid must be >0

    asteroids.remove((cx, cy))  # Remove the asteroid we're on, otherwise we'll never finish
    i = 1

    while asteroids:
        visibles = get_visibles(cx, cy, asteroids)
        destroyed = min(visibles, key=lambda asteroid: get_rel_angle((cx, cy), asteroid, rot))
        add_rot = get_rel_angle((cx, cy), destroyed, rot)
        rot += add_rot
        if rot >= 2 * math.pi:
            rot -= 2 * math.pi
        print("{:3d}: {:8s} -> rot + {:7.3f}° = {:7.3f}°".format(
            i, str(destroyed), add_rot / math.pi * 180, rot / math.pi * 180)
        )
        i += 1
        asteroids.remove(destroyed)


if __name__ == '__main__':
    main()
