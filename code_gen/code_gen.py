"""
Leo Kivikunnas 525925
Jaakko Koskela 526050
"""

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


class CodeGenerator:
    def __init__(self, symbol_table, scope_stack):
        self.symbol_table = symbol_table
        self.scope_stack = scope_stack
        self.semantic_stack = []

        # Address spaces
        self.variables_lower = 100
        self.variables_upper = 499
        self.temporaries_lower = 500
        self.temporaries_upper = 1000

        # Next addres to allocate
        self.next_var_addr = self.variables_lower
        self.next_temp_addr = self.temporaries_lower

        # The next assignment rhs is assigning an immediate value
        self.assigning_immediate = False

        self.output_lineno = 0
        self.output = []

    def format_operand(self, operand, operand_type):
        if operand_type == OperandTypes.ADDRESSING:
            return str(operand)
        elif operand_type == OperandTypes.INDIRECT_ADDRESSING:
            return f"@{operand}"
        elif operand_type == OperandTypes.IMMEDIATE:
            return f"#{operand}"

    def generate_3ac(self, operation=None, operands=[], operand_types=[]):
        formatted_operands = []
        for i, operand in enumerate(operands):
            formatted_operands.append(self.format_operand(operand, operand_types[i]))

        if operation == ThreeAddressCodes.ADD and len(operands) == 3:
            return f"{self.output_lineno}\t(ADD, {formatted_operands[0]}, {formatted_operands[1]}, {formatted_operands[2]})"
        elif operation == ThreeAddressCodes.ASSIGN and len(operands) == 2:
            return f"{self.output_lineno}\t(ASSIGN, {formatted_operands[0]}, {formatted_operands[1]}, )"

    def find_addr(self, symbol):
        idx = get_symbol_table_index(self.symbol_table, symbol)
        return self.symbol_table[idx]["address"]

    def increment_var_addr(self, n=4):
        self.next_var_addr += n
        self.next_var_addr %= self.variables_upper

    def increment_temp_addr(self, n=4):
        self.next_temp_addr += n
        self.next_temp_addr %= self.temporaries_upper

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

    def array_size(self, input_ptr):
        # We are declaring a array of size input_ptr[1]
        # Reserve enough space
        if self.symbol_table[-1]["address"] is not None:
            self.increment_var_addr(4 * (int(input_ptr[1]) - 1))  # One 4 byte section was already allocated

    def use_pid(self, input_ptr):
        self.semantic_stack.append(self.find_addr(input_ptr[1]))

    def assign_immediate(self, input_ptr):
        self.semantic_stack.append(input_ptr[1])
        self.assigning_immediate = True

    def assign(self):
        if not self.assigning_immediate and len(self.semantic_stack) > 1:
            # ss head is address of variable/temporary that we want to assign
            operand_types = [OperandTypes.ADDRESSING, OperandTypes.ADDRESSING]
        elif self.assigning_immediate and len(self.semantic_stack) > 0:
            # ss head is an immediate value
            operand_types = [OperandTypes.IMMEDIATE, OperandTypes.ADDRESSING]
            self.assigning_immediate = False

        generated_3ac = self.generate_3ac(ThreeAddressCodes.ASSIGN, [self.semantic_stack[-1], self.semantic_stack[-2]], operand_types)
        self.output.append(generated_3ac)
        self.output_lineno += 1

    def semantic_actions(self, action_symbol, input_ptr):
        if action_symbol == "#VARIABLE":
            self.variable()
        elif action_symbol == "#FUNCTION":
            self.function()
        elif action_symbol == "#ARRAY_SIZE":
            self.array_size(input_ptr)
        elif action_symbol == "#USE_PID":
            self.use_pid(input_ptr)
        elif action_symbol == "#ASSIGN_IMMEDIATE":
            self.assign_immediate(input_ptr)
        elif action_symbol == "#ASSIGN":
            self.assign()
        else:
            pass

    def write_output_to_file(self):
        with open("output.txt", "w") as f:
            for o in self.output:
                f.write(f"{o}\n")

            f.close()
