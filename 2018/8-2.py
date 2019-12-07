import re
from argparse import ArgumentParser
import numpy as np


def read_int(f):
    r = 0
    while True:
        c = f.read(1)
        try:
            r = 10*r + int(c)
        except ValueError:
            return r


def read_node(f):
    num_children = read_int(f)
    num_metadata = read_int(f)
    children = [read_node(f) for n in range(num_children)]
    metadatas = [read_int(f) for n in range(num_metadata)]
    return children, metadatas


def get_value(node):
    children, metas = node
    if not children:
        return sum(metas)
    else:
        return sum(get_value(children[n-1]) for n in metas if 0 < n <= len(children))


def process(f):
    root = read_node(f)
    print(get_value(root))


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    with open(args.file, 'r') as f:
        process(f)


if __name__ == '__main__':
    main()
