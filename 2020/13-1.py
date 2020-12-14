from argparse import ArgumentParser

from util import timed


def get_bus_departure(now, bus_interval):
    departure = (now // bus_interval) * bus_interval
    if departure < now:
        departure += bus_interval
    return departure


def find_earliest_bus_departure(now, bus_intervals):
    return min(
        ((bus_interval, get_bus_departure(now, bus_interval)) for bus_interval in bus_intervals),
        key=lambda bd: bd[1]
    )


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="13-input.txt")
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        now = int(f.readline().strip())
        bus_intervals = [int(w) for w in f.readline().strip().split(',') if w != 'x']

    bus_id, bus_departure = find_earliest_bus_departure(now, bus_intervals)
    wait_time = bus_departure - now
    print(f"bus {bus_id} departure {bus_departure}, wait time {wait_time}")
    print(f"{bus_id * wait_time}")


if __name__ == '__main__':
    main()
