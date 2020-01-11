from argparse import ArgumentParser
from intvm import IntVM


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str, nargs="?", default="21-input.txt")
    args = argparse.parse_args()

    with open(args.file, "r") as f:
        program = [int(c) for c in f.read().split(',')]

    instructions = [ord(c) for c in "".join(l+"\n" for l in (
        # if a hole is at distance two, jump now
        "NOT B T",
        "OR T J",

        # if a hole is at distance three, jump now
        "NOT C T",
        "OR T J",

        # But only if there is ground at distance 4
        "AND D J",
        # And there is ground at distance 8
        "AND H J",

        # If we're about to walk into a hole, jump anyway
        "NOT A T",
        "OR T J",

        "RUN"
    ))]

    vm = IntVM(
        program,
        inputs=instructions,
        output_func=lambda s: print(chr(s), end='', flush=True) if s < 127 else print(s)
    )
    vm.run()


if __name__ == '__main__':
    main()
