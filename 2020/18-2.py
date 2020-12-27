from argparse import ArgumentParser
from itertools import accumulate


def lexer_iterator(s):
    cur_num = ''
    for c in s:
        if c.isspace():
            continue
        elif c.isdigit():
            cur_num += c
        else:
            if cur_num:
                yield int(cur_num)
            yield c
            cur_num = ''
    if cur_num:
        yield int(cur_num)


def _match_parens(token_it):
    while True:
        try:
            token = next(token_it)
            if token == '(':
                yield tuple(_match_parens(token_it))
            elif token == ')':
                return
            else:
                yield token
        except StopIteration:
            return


def _match_ops(ast):
    if isinstance(ast, int):
        return ast

    if len(ast) == 1:
        return _match_ops(ast[0])

    try:
        mult_idx = ast.index('*')
        return _match_ops(ast[:mult_idx]), '*', _match_ops(ast[mult_idx+1:])
    except ValueError:
        return _match_ops(ast[0]), ast[1], _match_ops(ast[2:])


def parse(line):
    return _match_ops(tuple(_match_parens(lexer_iterator(line))))


def evaluate(expression):
    if isinstance(expression, int):
        return expression
    elif len(expression) == 1:
        return evaluate(expression[0])
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
