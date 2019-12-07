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


def meta_sum_recursive(node):
    return node[1] + [meta for child in node[0] for meta in meta_sum_recursive(child)]


def process(f):
    root = read_node(f)
    print(sum(meta_sum_recursive(root)))


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    with open(args.file, 'r') as f:
        process(f)


if __name__ == '__main__':
    main()
