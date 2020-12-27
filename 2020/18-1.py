from argparse import ArgumentParser
from itertools import accumulate


def parse(line):
    line = line.strip().replace(" ", "")
    if line[-1] == ')':
        end = next(len(line)-n+1 for n, c in enumerate(
            accumulate(line[::-1], lambda s, c: s + (1 if c == ')' else (-1 if c == '(' else 0)), initial=0)
        ) if n > 0 and c == 0)

        expr_b = parse(line[end:-1])
        op_index = end-2
        if op_index <= 0:
            return expr_b
    else:
        try:
            end = next(len(line)-n for n, c in enumerate(line[::-1]) if c in ('*', '+'))
            expr_b = int(line[end:])
            op_index = end-1
        except StopIteration:
            return int(line)

    return parse(line[:op_index]), line[op_index], expr_b


def evaluate(expression):
    if isinstance(expression, int):
        return expression
    else:
        a, op, b = expression
        a, b = evaluate(a), evaluate(b)
        return a + b if op == '+' else a * b


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="18-input.txt")
    argparse.add_argument("--verbose", "-v", action="store_true")
    args = argparse.parse_args()

    with open(args.file, 'r') as f:
        expressions = [parse(line) for line in f]

    if args.verbose:
        for expression in expressions:
            print(expression)
            print(evaluate(expression))
    print(sum(evaluate(expression) for expression in expressions))


if __name__ == '__main__':
    main()
