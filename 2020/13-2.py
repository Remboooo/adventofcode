from argparse import ArgumentParser

from util import timed, egcd


def least_common_multiple_with_offset(a_period, a_offset, b_period, b_offset):
    a_offset = (-a_offset) % a_period
    b_offset = (-b_offset) % b_period
    gcd, s, t = egcd(a_period, b_period)
    pd_mult, pd_remainder = divmod(a_offset - b_offset, gcd)
    combined_period = a_period // gcd * b_period
    combined_phase = (a_offset - s * pd_mult * a_period) % combined_period
    return -combined_phase % combined_period, combined_period


@timed
def get_earliest_consecutive_departure(bus_ids):
    remaining_bus_ids = bus_ids[1:]
    total_offset = 0
    total_period = bus_ids[0]
    bus_offset = 0

    while remaining_bus_ids:
        bus_id = remaining_bus_ids[0]
        remaining_bus_ids = remaining_bus_ids[1:]
        bus_offset += 1
        if bus_id is not None:
            total_offset, total_period = least_common_multiple_with_offset(
                total_period, total_offset, bus_id, -bus_offset
            )

    return total_offset


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="13-input.txt")
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        f.readline()
        bus_ids = [int(w) if w != 'x' else None for w in f.readline().strip().split(',')]

    print(get_earliest_consecutive_departure(bus_ids))


if __name__ == '__main__':
    main()
