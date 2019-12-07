from argparse import ArgumentParser


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


def run(program, inputs):
    input_gen = iter(inputs)
    output_consumer = print

    pc = 0
    while True:
        opcode = program[pc] % 100
        modes = get_modes(program[pc] // 100)
        pc = ops[opcode](program, pc, modes, input_gen, output_consumer)
        if pc < 0:
            return program


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    argparse.add_argument("input", type=str, default="5", nargs="?")
    args = argparse.parse_args()

    with open(args.file, "r") as f:
        program = [int(c) for c in f.read().split(',')]
        inputs = [int(c) for c in args.input.split(',')]
        run(program, inputs)


if __name__ == '__main__':
    main()
