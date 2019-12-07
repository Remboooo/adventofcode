from collections import defaultdict

import re
from functools import reduce

from argparse import ArgumentParser
from datetime import datetime, timedelta

EVENT_REGEX = re.compile(r'\[(\d\d\d\d-\d\d-\d\d \d\d:\d\d)\] (.+)')
BEGIN_REGEX = re.compile(r'Guard #(\d+) begins shift')


class Shift:
    def __init__(self, guard, start):
        self.guard = guard
        self.start = start
        self.sleeps = []

    def get_asleep_midnight_minutes(self):
        result = [0] * 60
        for start, end in self.sleeps:
            for minute in range(start.minute, end.minute):
                result[minute] += 1
        return result


def process(data):
    guard_shifts = defaultdict(list)
    for shift in read_shifts(data):
        guard_shifts[shift.guard].append(shift)


    max_asleep_minutes = 0
    max_asleep_guard = None
    max_asleep_minute = None

    for guard, shifts in guard_shifts.items():
        minute_asleep_counts = [sum(minute_asleeps) for minute_asleeps in
                                zip(*(shift.get_asleep_midnight_minutes() for shift in shifts))]

        asleep_minutes = sum(minute_asleep_counts)
        if asleep_minutes > max_asleep_minutes:
            max_asleep_minutes = asleep_minutes
            max_asleep_guard = guard
            max_asleep_minute = minute_asleep_counts.index(max(minute_asleep_counts))

    print("#{}: {} minutes, most at {}, mult = {}".format(max_asleep_guard, max_asleep_minutes, max_asleep_minute,
                                                          max_asleep_guard * max_asleep_minute))


def read_shifts(data):
    stamped_rows = []
    for row in data:
        match = EVENT_REGEX.fullmatch(row)
        if not match:
            raise ValueError("No match: {}".format(row))
        stamp = datetime.strptime(match[1], "%Y-%m-%d %H:%M")
        stamped_rows.append((stamp, match[2]))
    shifts = []
    current_shift = None
    sleep_start = None
    for timestamp, event in sorted(stamped_rows):
        match = BEGIN_REGEX.fullmatch(event)
        if match:
            if current_shift is not None:
                shifts.append(current_shift)
            current_shift = Shift(int(match[1]), timestamp)
            sleep_start = None
        elif event == 'falls asleep':
            sleep_start = timestamp
        elif event == 'wakes up':
            current_shift.sleeps.append((sleep_start, timestamp))
    return shifts


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        data = [l.strip() for l in f]
    process(data)


if __name__ == '__main__':
    main()

