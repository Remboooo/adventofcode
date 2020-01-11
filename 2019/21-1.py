from argparse import ArgumentParser
from intvm import IntVM


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str, nargs="?", default="21-input.txt")
    args = argparse.parse_args()

    with open(args.file, "r") as f:
        program = [int(c) for c in f.read().split(',')]

    instructions = [ord(c) for c in "".join(l+"\n" for l in (
        "NOT A J",  # jump if we're about to walk into a hole

        # if a hole is at distance two and there is ground at distance four,
        # jump now because maybe distance five is a hole
        "NOT B T",
        "AND D T",
        "OR T J",

        # if a hole is at distance three and there is ground at distance four,
        # jump now because maybe distance five is a hole
        "NOT C T",
        "AND D T",
        "OR T J",

        "WALK"
    ))]

    vm = IntVM(
        program,
        inputs=instructions,
        output_func=lambda s: print(chr(s), end='', flush=True) if s < 127 else print(s)
    )
    vm.run()


if __name__ == '__main__':
    main()
