from argparse import ArgumentParser


def process(data):
    def dataloop():
        while True:
            for x in data:
                yield x

    accumulated = set()
    freq = 0

    for x in dataloop():
        accumulated.add(freq)
        freq += x
        if freq in accumulated:
            print(freq)
            return


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        data = [int(l) for l in f]
    process(data)


if __name__ == '__main__':
    main()

