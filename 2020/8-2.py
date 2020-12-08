from argparse import ArgumentParser

from util import timed


class VM:
    def __init__(self, instructions):
        self.instructions = instructions
        self.visited_instructions = []
        self.pc = 0
        self.accumulator = 0

    def run(self):
        self.visited_instructions = [False for i in self.instructions]
        while True:
            self.visited_instructions[self.pc] = True
            inst, args = self.instructions[self.pc]
            self.pc = inst(self, *args)
            if self.pc >= len(self.visited_instructions):
                return True
            if self.visited_instructions[self.pc]:
                return False


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


def parse_program(f):
    return [parse_instruction(line.strip()) for line in f]


def find_jmp_nop_swap(instructions):
    for swap_pc in range(len(instructions)):
        if instructions[swap_pc][0] == _nop:
            swap_inst = _jmp
        elif instructions[swap_pc][0] == _jmp:
            swap_inst = _nop
        else:
            continue

        vm = VM([
            (i, args) if pc != swap_pc else (swap_inst, args)
            for pc, (i, args) in enumerate(instructions)]
        )

        if vm.run():
            return vm.accumulator


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", nargs='?', type=str, default="8-input.txt")
    args = argparse.parse_args()
    with open(args.file, "r") as f:
        program = parse_program(f)
        print(timed(find_jmp_nop_swap)(program))


if __name__ == '__main__':
    main()
