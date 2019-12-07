from argparse import ArgumentParser


def run(program, ops):
    pc = 0
    while True:
        opcode = program[pc]
        pc = ops[opcode](program, pc)
        if pc < 0:
            return program


def op_add(program, pc):
    program[program[pc + 3]] = program[program[pc + 1]] + program[program[pc + 2]]
    return pc + 4


def op_mul(program, pc):
    program[program[pc + 3]] = program[program[pc + 1]] * program[program[pc + 2]]
    return pc + 4


def op_hlt(program, pc):
    return -1


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()

    ops = {
        1: op_add,
        2: op_mul,
        99: op_hlt
    }

    with open(args.file, "r") as f:
        program_orig = [int(c) for c in f.read().split(',')]
        for noun in range(100):
            for verb in range(100):
                program = program_orig.copy()
                program[1] = noun
                program[2] = verb
                run(program, ops)
                print("{:02d}{:02d}: {}".format(noun, verb, program[0]))
                if program[0] == 19690720:
                    print(program)
                    print("answer = {:02d}{:02d}".format(noun, verb))
                    return


if __name__ == '__main__':
    main()
