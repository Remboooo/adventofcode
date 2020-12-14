from argparse import ArgumentParser

from util import timed


def least_common_multiple_with_offset(a, b):
    """
    Calculates the least common multiple with an offset of 1, i.e.:
    x = n*a+1 = m*b

    According to https://cs.stackexchange.com/questions/83689/how-to-calculate-least-common-multiple-lcm-for-two-numbers-with-constants-shi
    any solution must satisfy:
    n = -1 / a (mod b)
    and
    m = 1 / b (mod a)
    """
    inva = modinv(a, b)
    print(f"{a}^-1 mod {b} = {inva}")
    n = (-1 * inva) % b

    invb = modinv(b, a)
    print(f"{b}^-1 mod {a} = {invb}")
    m = (-1 * invb) % a

    print(f"{n} = -1 / {a} (mod {b})")
    print(f"{m} = -1 / {b} (mod {a})")
    print(f"{n} * {a} + 1 = {n*a+1}")
    print(f"{m} * {b} = {m * b}")


def modinv(x, p):
    """
    Calculates the modular inverse; x^-1 mod p
    """
    return pow(x, -1, p)


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="13-input.txt")
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        now = int(f.readline().strip())
        bus_intervals = [int(w) for w in f.readline().strip().split(',') if w != 'x']

    least_common_multiple_with_offset(7, 13)


if __name__ == '__main__':
    main()
