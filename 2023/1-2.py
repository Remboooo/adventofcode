from argparse import ArgumentParser

names = {
    "zero": 0,
    "one": 1,
    "two": 2,
    "three": 3,
    "four": 4,
    "five": 5,
    "six": 6,
    "seven": 7,
    "eight": 8,
    "nine": 9
}

if __name__ == '__main__':
    argparse = ArgumentParser()
    argparse.add_argument("input", type=str)
    args = argparse.parse_args()

    result = 0

    with open(args.input, 'r') as f:
        while line := f.readline():
            nums = [(i, c) for i, c in enumerate(line) if c.isnumeric()]
            alnums = [(i, str(v)) for i in range(len(line)) for k, v in names.items() if line[i:].startswith(k)]
            all = sorted([*nums, *alnums])
            numstart = all[0][1]
            numend = all[-1][1]
            result += int(numstart+numend)

    print(result)