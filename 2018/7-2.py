import re
from argparse import ArgumentParser

DEP_REGEX = re.compile(r'Step ([A-Z]) must be finished before step ([A-Z]) can begin\.')


def dependency(s):
    match = DEP_REGEX.fullmatch(s.strip())
    if not match:
        raise ValueError("Not a valid dependency: {}".format(s))
    return match[1], match[2]


class Worker:
    def __init__(self):
        self.task = None
        self.time_left = 0

    def tick(self):
        if self.task is None:
            return
        self.time_left -= 1
        if self.time_left == 0:
            task = self.task
            self.task = None
            return task

    def is_free(self):
        return self.task is None

    def assign(self, task):
        self.task = task
        self.time_left = 61 + (ord(task) - ord('A'))

    def letter(self):
        return self.task if self.task is not None else '.'


def process(data):
    steps = {s for row in data for s in row}
    do_first = {step: set() for step in steps}
    for finish, before in data:
        do_first[before].add(finish)

    sequence = []
    workers = [Worker() for n in range(5)]
    second = 0

    while True:
        if not do_first and not [w for w in workers if not w.is_free()]:
            break

        can_do_now = sorted({step for step, deps in do_first.items() if not deps})
        while can_do_now:
            do_now = can_do_now[0]
            free_workers = [w for w in workers if w.is_free()]
            if free_workers:
                free_workers[0].assign(do_now)
                del do_first[do_now]
            can_do_now = can_do_now[1:]

        print("{}  {}  {}".format(second, ' '.join(w.letter() for w in workers), ''.join(sequence)))

        second += 1

        for worker in workers:
            finished = worker.tick()
            if finished:
                sequence.append(finished)
                for deps in do_first.values():
                    deps.discard(finished)

    print(second)
    print(''.join(sequence))


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    with open(args.file, 'r') as f:
        data = [dependency(s) for s in f]
        process(data)


if __name__ == '__main__':
    main()
