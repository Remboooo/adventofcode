from argparse import ArgumentParser


def get_fuel(mass):
    fuel = max(0, mass // 3 - 2)
    if fuel > 0:
        fuel += get_fuel(fuel)
    return fuel


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        print(sum(get_fuel(int(l)) for l in f))


if __name__ == '__main__':
    main()
