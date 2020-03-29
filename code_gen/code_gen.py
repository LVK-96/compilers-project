"""
Jaakko Koskela 526050
"""
import pprint
from enum import Enum
from scanner import get_symbol_table_index, SymbolType


class ThreeAddressCodes(Enum):
    ADD = 1
    MULT = 2
    SUB = 3
    AND = 4
    NOT = 5
    EQ = 6
    LT = 7
    ASSIGN = 8
    JPF = 9
    JP = 10
    PRINT = 11


class OperandTypes(Enum):
    ADDRESSING = 1
    INDIRECT_ADDRESSING = 2
    IMMEDIATE = 3
    JP_LINENO = 4


class SSTypes(Enum):
    ADDRESS = 1
    IMMEDIATE = 2
    LINENO = 3


class CodeGenerator:
    def __init__(self, symbol_table, scope_stack):
        self.symbol_table = symbol_table
        self.scope_stack = scope_stack

        # Semnatic stack holds arrays of format [value, flag]
        self.semantic_stack = []

        # Address spaces
        self.variables_lower = 100
        self.variables_upper = 499
        self.temporaries_lower = 500
        self.temporaries_upper = 1000

        self.temps = [None] * (1 + self.temporaries_upper - self.temporaries_lower)

        # Next addres to allocate
        self.next_var_addr = self.variables_lower
        self.next_temp_addr = self.temporaries_lower

        # Name of the function we are currently in
        self.current_function = None

        self.function_call_stack = []

        # Linenumbers of functions in output, used for making the jumps
        self.function_linenos = {}
        # Addresses of temps holding function return values
        self.function_return_value_addrs = {}

        # Is the addop + or -
        self.addop_type = None

        self.output_lineno = 0
        self.output = []

    def get_temp_by_addr(self, addr):
        assert addr >= 500 and addr <= 1000
        return self.temps[addr - 500]

    def format_operand(self, operand, operand_type):
        if operand_type == OperandTypes.ADDRESSING or operand_type == OperandTypes.JP_LINENO:
            return str(operand)
        elif operand_type == OperandTypes.INDIRECT_ADDRESSING:
            return f"@{operand}"
        elif operand_type == OperandTypes.IMMEDIATE:
            return f"#{operand}"

    def generate_3ac(self, operation=None, operands=[], operand_types=[], backpatch=None):
        correct_lineno = self.output_lineno
        if backpatch is not None:
            correct_lineno = backpatch

        formatted_operands = []
        for i, operand in enumerate(operands):
            formatted_operands.append(self.format_operand(operand, operand_types[i]))

        if operation == ThreeAddressCodes.ADD and len(operands) == 3:
            return f"{correct_lineno}\t(ADD, {formatted_operands[0]}, {formatted_operands[1]}, {formatted_operands[2]})"
        elif operation == ThreeAddressCodes.SUB and len(operands) == 3:
            return f"{correct_lineno}\t(SUB, {formatted_operands[0]}, {formatted_operands[1]}, {formatted_operands[2]})"
        elif operation == ThreeAddressCodes.MULT and len(operands) == 3:
            return f"{correct_lineno}\t(MULT, {formatted_operands[0]}, {formatted_operands[1]}, {formatted_operands[2]})"
        elif operation == ThreeAddressCodes.ASSIGN and len(operands) == 2:
            return f"{correct_lineno}\t(ASSIGN, {formatted_operands[0]}, {formatted_operands[1]}, )"
        elif operation == ThreeAddressCodes.JP and len(operands) == 1:
            return f"{correct_lineno}\t(JP, {formatted_operands[0]}, , )"

    def find_addr(self, symbol):
        idx = get_symbol_table_index(self.symbol_table, symbol)
        return self.symbol_table[idx]["address"]

    def increment_var_addr(self, n=4):
        self.next_var_addr += n
        self.next_var_addr %= self.variables_upper

    def increment_temp_addr(self, n=4):
        self.next_temp_addr += n
        self.next_temp_addr %= self.temporaries_upper

    def start(self):
        # First thing to execute is always a jump into main, make room for that
        self.output.append(None)
        self.output_lineno += 1

    def end(self):
        # backpatch jump to main
        self.output[0] = self.generate_3ac(
            ThreeAddressCodes.JP, [
                self.function_linenos["main"]], [
                OperandTypes.JP_LINENO], backpatch=0)

    def variable(self):
        # Variable just declared is at the head of the symbol_table
        # Assign an address to the variable
        if self.symbol_table[-1]["address"] is None:
            self.symbol_table[-1]["address"] = self.next_var_addr
            self.increment_var_addr()

    def function(self):
        # Function just declared is at the head of the symbol table
        # Functions dont have addresses so remove address field from dict
        if (
            self.symbol_table[-1]["type"] in [SymbolType.FUNCTION_INT, SymbolType.FUNCTION_VOID]
            and "address" in self.symbol_table[-1].keys()
        ):
            del self.symbol_table[-1]["address"]

        # Whatever comes next is the first line of this function
        # Store it for possible later function calls so we can jump to this line
        self.function_linenos[self.symbol_table[-1]["name"]] = self.output_lineno

        # Keep track of the function we are currently generating code for
        self.current_function = self.symbol_table[-1]["name"]

    def array_size(self, input_ptr):
        # We are declaring a array of size input_ptr[1]
        # Reserve enough space
        if self.symbol_table[-1]["address"] is not None:
            self.increment_var_addr(4 * (int(input_ptr[1]) - 1))  # One 4 byte section was already allocated

    def use_pid(self, input_ptr):
        idx = get_symbol_table_index(self.symbol_table, input_ptr[1])
        if self.symbol_table[idx]["type"] not in [SymbolType.FUNCTION_INT, SymbolType.FUNCTION_VOID]:
            self.semantic_stack.append([self.find_addr(input_ptr[1]), SSTypes.ADDRESS])
        else:
            # Store function name in called_function for jump into said function in #FUNCTION_CALL
            self.function_call_stack.append(input_ptr[1])

    def immediate(self, input_ptr):
        self.semantic_stack.append([int(input_ptr[1]), SSTypes.IMMEDIATE])

    def indexing_done(self):
        # ss head is the address of the temp or the immediate value that is used as the index
        # ss head - 1 is the address of the array we are indexing
        if self.semantic_stack[-1][1] == SSTypes.IMMEDIATE:
            # Indexing using an immediate
            arr_idx = self.semantic_stack.pop()
            arr_idx = arr_idx[0]
        elif self.semantic_stack[-1][1] == SSTypes.ADDRESS:
            arr_idx = self.semantic_stack.pop()
            arr_idx = self.get_temp_by_addr(arr_idx[0])

        self.semantic_stack[-1][0] += (arr_idx * 4)

    def assign(self):
        if self.semantic_stack[-1][1] == SSTypes.IMMEDIATE:
            # ss head is an immediate value
            operand_types = [OperandTypes.IMMEDIATE, OperandTypes.ADDRESSING]
        elif self.semantic_stack[-1][1] == SSTypes.ADDRESS:
            # ss head is address of variable/temporary that we want to assign
            operand_types = [OperandTypes.ADDRESSING, OperandTypes.ADDRESSING]

        generated_3ac = self.generate_3ac(ThreeAddressCodes.ASSIGN,
                                          [self.semantic_stack[-1][0], self.semantic_stack[-2][0]],
                                          operand_types)
        self.output.append(generated_3ac)
        self.output_lineno += 1
        del self.semantic_stack[-2:]

    def plus(self):
        self.addop_type = "+"

    def minus(self):
        self.addop_type = "-"

    def addop(self):
        if self.addop_type == "+":
            operation = ThreeAddressCodes.ADD
        elif self.addop_type == "-":
            operation = ThreeAddressCodes.SUB

        if self.semantic_stack[-2][1] == SSTypes.IMMEDIATE:
            operand1_type = OperandTypes.IMMEDIATE
        elif self.semantic_stack[-2][1] == SSTypes.ADDRESS:
            operand1_type = OperandTypes.ADDRESSING

        if self.semantic_stack[-1][1] == SSTypes.IMMEDIATE:
            operand2_type = OperandTypes.IMMEDIATE
        elif self.semantic_stack[-1][1] == SSTypes.ADDRESS:
            operand2_type = OperandTypes.ADDRESSING

        generated_3ac = self.generate_3ac(operation,
                                          [self.semantic_stack[-2][0], self.semantic_stack[-1][0], self.next_temp_addr],
                                          [operand1_type, operand2_type, OperandTypes.ADDRESSING])
        self.output.append(generated_3ac)
        self.output_lineno += 1
        del self.semantic_stack[-2:]

        self.semantic_stack.append([self.next_temp_addr, SSTypes.ADDRESS])
        self.increment_temp_addr()
        self.addop_type = None

    def mult(self):
        if self.semantic_stack[-2][1] == SSTypes.IMMEDIATE:
            operand1_type = OperandTypes.IMMEDIATE
        elif self.semantic_stack[-2][1] == SSTypes.ADDRESS:
            operand1_type = OperandTypes.ADDRESSING

        if self.semantic_stack[-1][1] == SSTypes.IMMEDIATE:
            operand2_type = OperandTypes.IMMEDIATE
        elif self.semantic_stack[-1][1] == SSTypes.ADDRESS:
            operand2_type = OperandTypes.ADDRESSING

        generated_3ac = self.generate_3ac(ThreeAddressCodes.MULT,
                                          [self.semantic_stack[-2][0], self.semantic_stack[-1][0], self.next_temp_addr],
                                          [operand1_type, operand2_type, OperandTypes.ADDRESSING])
        self.output.append(generated_3ac)
        self.output_lineno += 1
        del self.semantic_stack[-2:]

        self.semantic_stack.append([self.next_temp_addr, SSTypes.ADDRESS])
        self.increment_temp_addr()

    def function_call(self):
        if self.function_call_stack[-1][0] != "output":
            # Backpatch jump back to caller from function
            generated_3ac = self.generate_3ac(ThreeAddressCodes.JP,
                                              [self.output_lineno + 1],
                                              [OperandTypes.JP_LINENO],
                                              backpatch=self.semantic_stack[-2][0])
            self.output[self.semantic_stack[-2][0]] = generated_3ac
            del self.semantic_stack[-2]

            # Get the address of the return value into the ss
            self.semantic_stack.append([self.function_return_value_addrs[self.function_call_stack[-1]], SSTypes.ADDRESS])

            # Jump to called function
            generated_3ac = self.generate_3ac(ThreeAddressCodes.JP,
                                              [self.function_linenos[self.function_call_stack[-1]]],
                                              [OperandTypes.JP_LINENO])
            self.function_call_stack.pop()
            self.output.append(generated_3ac)
            self.output_lineno += 1

    def ret(self):
        # Store return value here for later use if this function get called
        self.function_return_value_addrs[self.current_function] = self.next_temp_addr

        # Assign return value into a temp
        if self.semantic_stack[-1][1] == SSTypes.IMMEDIATE:
            operand_types = [OperandTypes.IMMEDIATE, OperandTypes.ADDRESSING]
        elif self.semantic_stack[-1][1] == SSTypes.ADDRESS:
            operand_types = [OperandTypes.ADDRESSING, OperandTypes.ADDRESSING]

        generated_3ac = self.generate_3ac(ThreeAddressCodes.ASSIGN,
                                          [self.semantic_stack[-1][0], self.next_temp_addr],
                                          operand_types)
        self.output.append(generated_3ac)
        self.output_lineno += 1
        self.semantic_stack.pop()
        self.increment_temp_addr()

        # Save space for jump back to previous function
        self.output.append(None)
        self.semantic_stack.append([self.output_lineno, SSTypes.LINENO])
        self.output_lineno += 1

        # We are ending code gen for this function
        self.curren_function = None

    def semantic_actions(self, action_symbol, input_ptr):
        if action_symbol == "#START":
            self.start()
        if action_symbol == "#END":
            self.end()
        elif action_symbol == "#VARIABLE":
            self.variable()
        elif action_symbol == "#FUNCTION":
            self.function()
        elif action_symbol == "#ARRAY_SIZE":
            self.array_size(input_ptr)
        elif action_symbol == "#USE_PID":
            self.use_pid(input_ptr)
        elif action_symbol == "#IMMEDIATE":
            self.immediate(input_ptr)
        elif action_symbol == "#INDEXING_DONE":
            self.indexing_done()
        elif action_symbol == "#ASSIGN":
            self.assign()
        elif action_symbol == "#PLUS":
            self.plus()
        elif action_symbol == "#MINUS":
            self.minus()
        elif action_symbol == "#ADDOP":
            self.addop()
        elif action_symbol == "#MULT":
            self.mult()
        elif action_symbol == "#FUNCTION_CALL":
            self.function_call()
        elif action_symbol == "#RETURN":
            self.ret()
        elif action_symbol == "#ENDSCOPE":
            # print(self.semantic_stack)
            # print()
            pass
        else:
            pass

    def write_output_to_file(self):
        with open("output.txt", "w") as f:
            for o in self.output:
                f.write(f"{o}\n")

            f.close()
