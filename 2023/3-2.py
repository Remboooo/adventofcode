from argparse import ArgumentParser
import re


def load_schematic():
    with open(args.input, 'r') as f:
        nums = []
        syms = []
        y = 0
        while line := f.readline():
            num = ''
            for x, c in enumerate(line.strip() + '.'):
                if c.isnumeric():
                    num += c
                else:
                    if num:
                        nums.append((num, (x - len(num), y)))
                        num = ''
                    if c != '.':
                        syms.append((c, (x, y)))
            y += 1
    return nums, syms


if __name__ == '__main__':
    argparse = ArgumentParser()
    argparse.add_argument("input", type=str)
    args = argparse.parse_args()

    result = 0

    nums, syms = load_schematic()

    result = 0

    for sym, (sym_x, sym_y) in syms:
        if sym != '*':
            continue
        gear_nums = []
        for num, (num_x, num_y) in nums:
            if sym_y < num_y-1 or sym_y > num_y + 1:
                continue
            if sym_x < num_x - 1 or sym_x > num_x + len(num):
                continue
            gear_nums.append(int(num))
        if len(gear_nums) == 2:
            result += gear_nums[0] * gear_nums[1]

    print(result)

