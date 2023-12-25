from argparse import ArgumentParser
import re
from collections import defaultdict
from functools import reduce

line_re = re.compile(r"^Game (\d+): (.+)$")
cube_re = re.compile(r"^(\d+) (.+)$")


def get_min_power(game_grabs):
    col_nums = defaultdict(list)
    for grab in game_grabs.split("; "):
        for cube in grab.split(", "):
            cube_match = cube_re.match(cube)
            cube_num = int(cube_match.group(1))
            cube_col = cube_match.group(2)
            col_nums[cube_col].append(cube_num)

    return reduce(lambda x, y: x * y, (max(vals) for vals in col_nums.values()), 1)


if __name__ == '__main__':
    argparse = ArgumentParser()
    argparse.add_argument("input", type=str)
    args = argparse.parse_args()

    result = 0

    with open(args.input, 'r') as f:
        while line := f.readline():
            match = line_re.match(line.strip())
            game_nr = int(match.group(1))
            game_grabs = match.group(2)
            power = get_min_power(game_grabs)
            print(power)
            result += power
    print()
    print(result)