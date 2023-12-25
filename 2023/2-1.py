from argparse import ArgumentParser
import re

line_re = re.compile(r"^Game (\d+): (.+)$")
cube_re = re.compile(r"^(\d+) (.+)$")

test = {"red": 12, "green": 13, "blue": 14}


def is_possible(game_grabs):
    for grab in game_grabs.split("; "):
        for cube in grab.split(", "):
            cube_match = cube_re.match(cube)
            cube_num = int(cube_match.group(1))
            cube_col = cube_match.group(2)
            if cube_num > test[cube_col]:
                return False
    return True


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
            if is_possible(game_grabs):
                print(game_nr)
                result += game_nr
    print()
    print(result)