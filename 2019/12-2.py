import re
from argparse import ArgumentParser
from itertools import permutations, count
from math import gcd

POS_RE = re.compile(r'<x=(?P<x>-?\d+), y=(?P<y>-?\d+), z=(?P<z>-?\d+)>')


class Moon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0
        self.vy = 0
        self.vz = 0


def lcm(*numbers):
    result = numbers[0]
    for i in numbers[1:]:
        result = result * i // gcd(result, i)
    return result


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        moons = [Moon(int(d['x']), int(d['y']), int(d['z']))
                 for d in (d.groupdict()
                           for d in (POS_RE.fullmatch(line.strip())
                                     for line in f.readlines()) if d)]

    period_x = 0
    period_y = 0
    period_z = 0

    for i in count(1):
        for moon1, moon2 in permutations(moons, 2):
            moon1.vx += +1 if moon2.x > moon1.x else -1 if moon2.x < moon1.x else 0
            moon1.vy += +1 if moon2.y > moon1.y else -1 if moon2.y < moon1.y else 0
            moon1.vz += +1 if moon2.z > moon1.z else -1 if moon2.z < moon1.z else 0

        for moon in moons:
            moon.x += moon.vx
            moon.y += moon.vy
            moon.z += moon.vz

        if not period_x and sum(abs(m.vx) for m in moons) == 0:
            period_x = i
            print("x: {}".format(i))
        if not period_y and sum(abs(m.vy) for m in moons) == 0:
            period_y = i
            print("y: {}".format(i))
        if not period_z and sum(abs(m.vz) for m in moons) == 0:
            period_z = i
            print("z: {}".format(i))

        if period_x and period_y and period_z:
            break

    print(2 * lcm(period_x, period_y, period_z))


if __name__ == '__main__':
    main()
