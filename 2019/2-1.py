from argparse import ArgumentParser


def run(program):
    pc = 0
    while True:
        opcode = program[pc]
        ops = program[pc+1:pc+4]
        print("@{}: {} -> {}".format(pc, opcode, ops))
        if opcode == 1:
            program[ops[2]] = program[ops[0]] + program[ops[1]]
        elif opcode == 2:
            program[ops[2]] = program[ops[0]] * program[ops[1]]
        elif opcode == 99:
            return program
        else:
            print("Unknown opcode {}, PC={}".format(opcode, pc))
        pc += 4


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        program = [int(c) for c in f.read().split(',')]
        program[1] = 12
        program[2] = 2
        print(program)
        run(program)
        print(program)
        print("answer = {}".format(program[0]))


if __name__ == '__main__':
    main()
