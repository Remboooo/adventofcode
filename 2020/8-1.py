from argparse import ArgumentParser

from util import timed


class Program:
    def __init__(self, instructions):
        self.instructions = instructions

    @staticmethod
    def parse(f):
        return Program([parse_instruction(line.strip()) for line in f])


class VM:
    def __init__(self, program: Program):
        self.program = program
        self.visited_instructions = []
        self.pc = 0
        self.accumulator = 0

    def run(self):
        self.visited_instructions = [False for i in self.program.instructions]
        while True:
            self.visited_instructions[self.pc] = True
            inst, args = self.program.instructions[self.pc]
            self.pc = inst(self, *args)
            if self.visited_instructions[self.pc]:
                break


def _acc(vm: 'VM', arg):
    vm.accumulator += arg
    return vm.pc + 1


def _jmp(vm: 'VM', arg):
    return vm.pc + arg


def _nop(vm: 'VM', arg):
    return vm.pc + 1


INSTRUCTION_MAP = {
    'acc': _acc,
    'jmp': _jmp,
    'nop': _nop,
}


def parse_instruction(line):
    words = line.split(' ')
    return INSTRUCTION_MAP[words[0]], tuple(int(w) for w in words[1:])


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="8-input.txt")
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        program = Program.parse(f)
        vm = VM(program)
        timed(vm.run)()
        print(vm.accumulator)


if __name__ == '__main__':
    main()
