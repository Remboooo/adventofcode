import re
from argparse import ArgumentParser
from itertools import permutations

POS_RE = re.compile(r'<x=(?P<x>-?\d+), y=(?P<y>-?\d+), z=(?P<z>-?\d+)>')


class Moon:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.vx = 0
        self.vy = 0
        self.vz = 0

    def kinetic_energy(self):
        return (abs(self.x) + abs(self.y) + abs(self.z)) * (abs(self.vx) + abs(self.vy) + abs(self.vz))

    def __str__(self):
        return "pos=<x={:3d}, y={:3d}, z={:3d}>, vel=<x={:3d}, y={:3d}, z={:3d}>".format(
            self.x, self.y, self.z, self.vx, self.vy, self.vz
        )


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    argparse.add_argument("steps", type=int, nargs="?", default=1000)
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        moons = [Moon(int(d['x']), int(d['y']), int(d['z']))
                 for d in (d.groupdict()
                           for d in (POS_RE.fullmatch(line.strip())
                                     for line in f.readlines()) if d)]

    print(moons)

    for i in range(args.steps):
        for moon1, moon2 in permutations(moons, 2):
            moon1.vx += +1 if moon2.x > moon1.x else -1 if moon2.x < moon1.x else 0
            moon1.vy += +1 if moon2.y > moon1.y else -1 if moon2.y < moon1.y else 0
            moon1.vz += +1 if moon2.z > moon1.z else -1 if moon2.z < moon1.z else 0

        for moon in moons:
            moon.x += moon.vx
            moon.y += moon.vy
            moon.z += moon.vz

        print("After {} steps:".format(i+1))
        for moon in moons:
            print(str(moon))
        print("Total energy: {}".format(sum(moon.kinetic_energy() for moon in moons)))


if __name__ == '__main__':
    main()
