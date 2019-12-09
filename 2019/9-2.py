from argparse import ArgumentParser
from collections import defaultdict
from itertools import permutations


class InfiniteArray(list):
    def __init__(self, initial_contents=None, fill_value=0):
        super().__init__(initial_contents if initial_contents else [])
        self.fill_value = fill_value

    def __getitem__(self, item):
        self._expand_to(item)
        return super().__getitem__(item)

    def __setitem__(self, key, value):
        self._expand_to(key)
        return super().__setitem__(key, value)

    def _expand_to(self, item):
        last_idx = item if isinstance(item, int) else item.stop
        app = (1 + last_idx - len(self))
        if app > 0:
            self.extend([self.fill_value] * app)


class ProgramState:
    def __init__(self, memory):
        self.memory = InfiniteArray(memory)
        self.relative_base = 0
        self.pc = 0


class IntVM:
    def __init__(self, program, inputs=None, output_func=print):
        self.state = ProgramState(program)
        self.input_gen = iter(inputs) if inputs is not None else []
        self.output_consumer = output_func

    def op_add(self, input_op_vals, output_op_addrs):
        self.state.memory[output_op_addrs[0]] = input_op_vals[0] + input_op_vals[1]

    def op_mul(self, input_op_vals, output_op_addrs):
        self.state.memory[output_op_addrs[0]] = input_op_vals[0] * input_op_vals[1]

    def op_input(self, input_op_vals, output_op_addrs):
        self.state.memory[output_op_addrs[0]] = next(self.input_gen)

    def op_output(self, input_op_vals, output_op_addrs):
        self.output_consumer(input_op_vals[0])

    def op_jump_if_true(self, input_op_vals, output_op_addrs):
        op_test, op_pc = input_op_vals
        if op_test != 0:
            return op_pc

    def op_jump_if_false(self, input_op_vals, output_op_addrs):
        op_test, op_pc = input_op_vals
        if op_test == 0:
            return op_pc

    def op_less_than(self, input_op_vals, output_op_addrs):
        op1, op2 = input_op_vals
        self.state.memory[output_op_addrs[0]] = 1 if op1 < op2 else 0

    def op_equals(self, input_op_vals, output_op_addrs):
        op1, op2 = input_op_vals
        self.state.memory[output_op_addrs[0]] = 1 if op1 == op2 else 0

    def op_adj_rel_base(self, input_op_vals, output_op_addrs):
        self.state.relative_base += input_op_vals[0]

    def op_hlt(self, input_op_vals, output_op_addrs):
        return -1

    def get_input_op_vals(self, op_modes, operands):
        modes = {
            0: lambda s, operand: s.memory[operand],
            1: lambda s, operand: operand,
            2: lambda s, operand: s.memory[s.relative_base + operand]
        }
        return [modes[mode](self.state, operand) for mode, operand in zip(op_modes, operands)]
    
    def get_output_op_addrs(self, op_modes, operands):
        modes = {
            0: lambda s, operand: operand,
            2: lambda s, operand: s.relative_base + operand
        }
        return [modes[mode](self.state, operand) for mode, operand in zip(op_modes, operands)]

    def get_modes(self, opcode, num_ops):
        def _m(opcode_mode):
            return [opcode_mode % 10] + _m(opcode_mode // 10) if opcode_mode != 0 else []

        op_modes = _m(opcode // 100)
        return [op_modes[i] if i < len(op_modes) else 0 for i in range(num_ops)]

    def run(self):
        self.state.pc = 0
        while True:
            opcode = self.state.memory[self.state.pc]

            op_func, num_input_ops, num_output_ops = self.ops[opcode % 100]
            op_modes = self.get_modes(opcode, num_input_ops + num_output_ops)

            input_modes = op_modes[:num_input_ops]
            input_ops = self.state.memory[self.state.pc+1:self.state.pc+1+num_input_ops]
            input_op_vals = self.get_input_op_vals(input_modes, input_ops)

            output_modes = op_modes[num_input_ops:num_input_ops + num_output_ops]
            output_ops = self.state.memory[self.state.pc+1+num_input_ops:self.state.pc+1+num_input_ops+num_output_ops]
            output_op_addrs = self.get_output_op_addrs(output_modes, output_ops)

            new_pc = op_func(self, input_op_vals, output_op_addrs)
            if new_pc is not None:
                self.state.pc = new_pc
            else:
                self.state.pc += 1 + num_input_ops + num_output_ops
            
            if self.state.pc < 0:
                return self.state

    ops = {
        1: (op_add, 2, 1),
        2: (op_mul, 2, 1),
        3: (op_input, 0, 1),
        4: (op_output, 1, 0),
        5: (op_jump_if_true, 2, 0),
        6: (op_jump_if_false, 2, 0),
        7: (op_less_than, 2, 1),
        8: (op_equals, 2, 1),
        9: (op_adj_rel_base, 1, 0),
        99: (op_hlt, 0, 0)
    }


class Container:
    def __init__(self, value):
        self.value = value


def main():
    argparse = ArgumentParser()
    argparse.add_argument("file", type=str)
    argparse.add_argument("input", type=str, default="2", nargs="?")
    args = argparse.parse_args()

    inputs = [int(c) for c in args.input.split(',')]

    with open(args.file, "r") as f:
        program = [int(c) for c in f.read().split(',')]

    IntVM(program, inputs).run()


if __name__ == '__main__':
    main()
