from argparse import ArgumentParser


if __name__ == '__main__':
    argparse = ArgumentParser()
    argparse.add_argument("input", type=str)
    args = argparse.parse_args()

    result = 0

    with open(args.input, 'r') as f:
        while line := f.readline():
            nums = [c for c in line if c.isnumeric()]
            result += int(nums[0] + nums[-1])

    print(result)