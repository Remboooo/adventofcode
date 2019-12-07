from argparse import ArgumentParser


def process(data):
    print(sum(data))


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        data = [int(l) for l in f]
    process(data)


if __name__ == '__main__':
    main()

