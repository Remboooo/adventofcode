from argparse import ArgumentParser
from itertools import permutations
from queue import Queue
from threading import Thread


def get_operands(program, pc, op_modes, num):
    op_modes = [op_modes[i] if i < len(op_modes) else 0 for i in range(num)]
    modes = {
        0: lambda program, operand: program[operand],
        1: lambda program, operand: operand
    }
    return [modes[op_modes[i]](program, program[pc + i + 1]) for i in range(num)]


def op_add(program, pc, modes, input_gen, output_consumer):
    op1, op2 = get_operands(program, pc, modes, 2)
    program[program[pc + 3]] = op1 + op2
    return pc + 4


def op_mul(program, pc, modes, input_gen, output_consumer):
    op1, op2 = get_operands(program, pc, modes, 2)
    program[program[pc + 3]] = op1 * op2
    return pc + 4


def op_input(program, pc, modes, input_gen, output_consumer):
    program[program[pc + 1]] = next(input_gen)
    return pc + 2


def op_output(program, pc, modes, input_gen, output_consumer):
    output_consumer(get_operands(program, pc, modes, 1)[0])
    return pc + 2


def op_jump_if_true(program, pc, modes, input_gen, output_consumer):
    op_test, op_pc = get_operands(program, pc, modes, 2)
    if op_test != 0:
        return op_pc
    else:
        return pc + 3


def op_jump_if_false(program, pc, modes, input_gen, output_consumer):
    op_test, op_pc = get_operands(program, pc, modes, 2)
    if op_test == 0:
        return op_pc
    else:
        return pc + 3


def op_less_than(program, pc, modes, input_gen, output_consumer):
    op1, op2 = get_operands(program, pc, modes, 2)
    program[program[pc + 3]] = 1 if op1 < op2 else 0
    return pc + 4


def op_equals(program, pc, modes, input_gen, output_consumer):
    op1, op2 = get_operands(program, pc, modes, 2)
    program[program[pc + 3]] = 1 if op1 == op2 else 0
    return pc + 4


def op_hlt(program, pc, modes, input_gen, output_consumer):
    return -1


ops = {
    1: op_add,
    2: op_mul,
    3: op_input,
    4: op_output,
    5: op_jump_if_true,
    6: op_jump_if_false,
    7: op_less_than,
    8: op_equals,
    99: op_hlt
}


def get_modes(opcode_mode):
    if opcode_mode == 0:
        return []
    else:
        return [opcode_mode % 10] + get_modes(opcode_mode // 10)


def run(program, inputs, output_consumer=print):
    program = program.copy()
    input_gen = iter(inputs)

    pc = 0
    while True:
        opcode = program[pc] % 100
        modes = get_modes(program[pc] // 100)
        pc = ops[opcode](program, pc, modes, input_gen, output_consumer)
        if pc < 0:
            return program


class IterableQueue(Queue):
    _sentinel = object()

    def __iter__(self):
        return iter(self.get, self._sentinel)

    def close(self):
        self.put(self._sentinel)


class Amplifier(Thread):
    def __init__(self, name, program, phase):
        super().__init__()
        self.name = name
        self.program = program
        self.phase = phase
        self.input_queue = None
        self.output_queue = IterableQueue()

    def run(self):
        self.input_queue.put(self.phase)
        run(self.program, self.input_queue, lambda val: self.output_queue.put(val))


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    args = argparse.parse_args()

    with open(args.file, "r") as f:
        program = [int(c) for c in f.read().split(',')]

    max_output = 0
    max_output_phases = []

    for phases in permutations(range(5, 10)):
        amps = [Amplifier(str(i), program, phase) for i, phase in enumerate(phases)]
        for i in range(len(amps)):
            amps[i].input_queue = amps[i-1].output_queue
            amps[i].start()

        amps[0].input_queue.put(0)

        for amp in amps:
            amp.join()

        output = amps[-1].output_queue.get()
        if output > max_output:
            max_output = output
            max_output_phases = list(phases)

    print("MAX: {} -> {}".format(max_output_phases, max_output))


if __name__ == '__main__':
    main()
