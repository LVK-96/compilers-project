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
    LINENO = 4


class CodeGenerator:
    def __init__(self, symbol_table, scope_stack):
        self.symbol_table = symbol_table
        self.scope_stack = scope_stack

        # Semantic stack holds arrays of format [value, flag]
        self.semantic_stack = []

        # Address spaces
        self.variables_lower = 100
        self.variables_upper = 499
        self.temporaries_lower = 500

        # Next addres to allocate
        self.next_var_addr = self.variables_lower
        self.next_temp_addr = self.temporaries_lower

        # Name of the function we are currently in
        self.current_function = []

        self.function_call_stack = []

        # Linenumbers of functions in output, used for making jumps
        self.function_linenos = {}
        # Addresses of function params
        self.function_params = {}
        # Addresses of temps holding function return values and linenos and return addresses of return jumps
        self.function_returns = {}

        # Is the return statement a empty return (return;)
        self.empty_ret_flag = False

        # How many chained assignments we have
        self.chained_assignments = 0

        # Array of saved linenos for breaks
        self.break_counter = []

        # Continue jump target
        self.continue_jump_target = []

        # Is the next case the first case
        self.first_case_next = []

        # Is the addop + or -
        self.addop_type = []
        # Is the relop < or ==
        self.relop_type = []

        self.output_lineno = 0
        self.output = []

    def format_operand(self, operand, operand_type):
        if operand_type == OperandTypes.ADDRESSING or operand_type == OperandTypes.LINENO:
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
            return (
                f"{correct_lineno}\t(MULT, {formatted_operands[0]}, {formatted_operands[1]}, {formatted_operands[2]})"
            )
        elif operation == ThreeAddressCodes.LT and len(operands) == 3:
            return f"{correct_lineno}\t(LT, {formatted_operands[0]}, {formatted_operands[1]}, {formatted_operands[2]})"
        elif operation == ThreeAddressCodes.EQ and len(operands) == 3:
            return f"{correct_lineno}\t(EQ, {formatted_operands[0]}, {formatted_operands[1]}, {formatted_operands[2]})"
        elif operation == ThreeAddressCodes.ASSIGN and len(operands) == 2:
            return f"{correct_lineno}\t(ASSIGN, {formatted_operands[0]}, {formatted_operands[1]}, )"
        elif operation == ThreeAddressCodes.JP and len(operands) == 1:
            return f"{correct_lineno}\t(JP, {formatted_operands[0]}, , )"
        elif operation == ThreeAddressCodes.JPF and len(operands) == 2:
            return f"{correct_lineno}\t(JPF, {formatted_operands[0]}, {formatted_operands[1]}, )"
        elif operation == ThreeAddressCodes.PRINT and len(operands) == 1:
            return f"{correct_lineno}\t(PRINT, {formatted_operands[0]}, , )"

    def find_addr(self, symbol):
        idx = get_symbol_table_index(self.symbol_table, symbol)
        return self.symbol_table[idx]["address"]

    def increment_var_addr(self, n=4):
        self.next_var_addr += n
        self.next_var_addr %= self.variables_upper

    def increment_temp_addr(self, n=4):
        self.next_temp_addr += n

    def backpatch_save(self):
        # Helper function for saving places for backpatching
        self.output.append(None)
        self.semantic_stack.append([self.output_lineno, OperandTypes.LINENO])
        self.output_lineno += 1

    def start(self):
        # First thing to execute is always a jump into main, make room for that
        self.backpatch_save()

    def end(self):
        # backpatch jump to main
        self.semantic_stack.pop()
        self.output[0] = self.generate_3ac(ThreeAddressCodes.JP,
                                           [self.function_linenos["main"]],
                                           [OperandTypes.LINENO], backpatch=0)

    def variable(self):
        # Variable just declared is at the head of the symbol_table
        # Assign an address to the variable
        if self.symbol_table[-1]["address"] is None:
            self.symbol_table[-1]["address"] = self.next_var_addr
            self.increment_var_addr()

    def function(self):
        # Function just declared is at the head of the symbol table
        # Functions dont have addresses so remove address field from the symbol table entry
        if (
            self.symbol_table[-1]["type"] in [SymbolType.FUNCTION_INT, SymbolType.FUNCTION_VOID]
            and "address" in self.symbol_table[-1].keys()
        ):
            del self.symbol_table[-1]["address"]

        # Keep track of the function we are currently generating code for
        self.current_function.append(self.symbol_table[-1]["name"])

    def statements_begin(self):
        # Whatever comes next is the first line of this function
        # Store it for possible later function calls so we can jump to this line
        if self.current_function[-1] not in self.function_linenos.keys():
            self.function_linenos[self.current_function[-1]] = self.output_lineno

    def end_scope(self):
        # We are ending code gen for the previous function (if there was one)
        # If there was no return just handle it like it was an empty return
        if self.current_function[-1] not in self.function_returns.keys():
            self.empty_ret_flag = True
            self.ret()

        self.current_function.pop()

    def stop_param_counter(self):
        idx = get_symbol_table_index(self.symbol_table, self.current_function[-1])
        no_params = len(self.symbol_table[idx]["params"])

        # The last no_params elements of the symbol table are function parameters
        if no_params > 0:
            params = self.symbol_table[-no_params:]
            self.function_params[self.current_function[-1]] = [[p["name"], p["address"], p["type"]] for p in params]
        else:
            self.function_params[self.current_function[-1]] = []

    def array_size(self, input_ptr):
        # We are declaring an array of size input_ptr[1]
        # Reserve enough space

        if self.symbol_table[-1]["address"] is not None:
            # Store arrays first addr in a temp, it is used for indirect addressing
            self.increment_var_addr(4 * (int(input_ptr[1]) - 1))  # One 4 byte section was already allocated

    def pid(self, input_ptr):
        idx = get_symbol_table_index(self.symbol_table, input_ptr[1])
        if self.symbol_table[idx]["type"] not in [SymbolType.FUNCTION_INT, SymbolType.FUNCTION_VOID]:
            addr = self.symbol_table[idx]["address"]
            if addr is None:
                # Address not yet allocated -> allocate it now
                addr = self.next_var_addr
                self.symbol_table[idx]["address"] = addr
                self.increment_var_addr()

    def use_pid(self, input_ptr):
        idx = get_symbol_table_index(self.symbol_table, input_ptr[1])
        if (
            idx is not None
            and self.symbol_table[idx]["type"] not in [SymbolType.FUNCTION_INT, SymbolType.FUNCTION_VOID]
        ):
            addr = self.symbol_table[idx]["address"]
            if addr is None:
                # Address not yet allocated -> allocate it now
                addr = self.next_var_addr
                self.symbol_table[idx]["address"] = addr
                self.increment_var_addr()

            self.semantic_stack.append([addr, OperandTypes.ADDRESSING])
        elif (
            (idx is not None and self.symbol_table[idx]["type"] in [SymbolType.FUNCTION_INT, SymbolType.FUNCTION_VOID])
            or input_ptr[1] == "output"
        ):
            # Store function name in called_function for jump into said function in #FUNCTION_CALL
            self.function_call_stack.append(input_ptr[1])

    def immediate(self, input_ptr):
        self.semantic_stack.append([int(input_ptr[1]), OperandTypes.IMMEDIATE])

    def indexing_done(self):
        # ss head is the address of the temp or the immediate value that is used as the index
        # ss head - 1 is the address of the array we are indexing
        # Calculate the offset
        offset_addr = self.next_temp_addr
        generated_3ac = self.generate_3ac(ThreeAddressCodes.MULT,
                                          [self.semantic_stack[-1][0], 4, offset_addr],
                                          [self.semantic_stack[-1][1], OperandTypes.IMMEDIATE, OperandTypes.ADDRESSING])
        self.output.append(generated_3ac)
        self.output_lineno += 1
        self.increment_temp_addr()

        # Add offset to the address of the array to get the address of the element
        # after this element addr holds the address of the element, we can use indirect addressing to access it
        array_name = [
            s["name"] for s in self.symbol_table if "address" in s.keys() and s["address"] == self.semantic_stack[-2][0]
        ][0]

        array_operand_type = OperandTypes.IMMEDIATE
        param_names = [p[0] for p in self.function_params[self.current_function[-1]]]
        if array_name in param_names:
            array_operand_type = OperandTypes.ADDRESSING

        element_addr = self.next_temp_addr
        generated_3ac = self.generate_3ac(ThreeAddressCodes.ADD,
                                          [self.semantic_stack[-2][0], offset_addr, element_addr],
                                          [array_operand_type, OperandTypes.ADDRESSING, OperandTypes.ADDRESSING])
        self.output.append(generated_3ac)
        self.output_lineno += 1
        self.increment_temp_addr()
        del self.semantic_stack[-2:]

        self.semantic_stack.append([element_addr, OperandTypes.INDIRECT_ADDRESSING])

    def assignment_chain(self):
        self.chained_assignments += 1

    def assign(self):
        generated_3ac = self.generate_3ac(ThreeAddressCodes.ASSIGN,
                                          [self.semantic_stack[-1][0], self.semantic_stack[-2][0]],
                                          [self.semantic_stack[-1][1], self.semantic_stack[-2][1]])
        self.output.append(generated_3ac)
        self.output_lineno += 1
        if self.chained_assignments < 2:
            self.chained_assignments -= 1
            del self.semantic_stack[-2:]
        else:
            self.chained_assignments -= 1
            self.semantic_stack.pop()

    def plus(self):
        self.addop_type.append("+")

    def minus(self):
        self.addop_type.append("-")

    def mathop(self, operation):
        # Common helper function for mathematical operations
        generated_3ac = self.generate_3ac(
            operation,
            [self.semantic_stack[-2][0], self.semantic_stack[-1][0], self.next_temp_addr],
            [self.semantic_stack[-2][1], self.semantic_stack[-1][1], OperandTypes.ADDRESSING]
        )
        self.output.append(generated_3ac)
        self.output_lineno += 1
        del self.semantic_stack[-2:]

        self.semantic_stack.append([self.next_temp_addr, OperandTypes.ADDRESSING])
        self.increment_temp_addr()

    def addop(self):
        if self.addop_type[-1] == "+":
            operation = ThreeAddressCodes.ADD
        elif self.addop_type[-1] == "-":
            operation = ThreeAddressCodes.SUB

        self.mathop(operation)
        self.addop_type.pop()

    def mult(self):
        self.mathop(ThreeAddressCodes.MULT)

    def lt(self):
        self.relop_type.append("<")

    def eq(self):
        self.relop_type.append("==")

    def relop(self):
        if self.relop_type[-1] == "<":
            operation = ThreeAddressCodes.LT
        elif self.relop_type[-1] == "==":
            operation = ThreeAddressCodes.EQ

        self.mathop(operation)
        self.relop_type.pop()

    def save(self):
        # Save space for jump
        self.backpatch_save()

    def jpf_save(self):
        # backpatch jpf to after if
        generated_3ac = self.generate_3ac(ThreeAddressCodes.JPF,
                                          [self.semantic_stack[-2][0], self.output_lineno + 1],
                                          [OperandTypes.ADDRESSING, OperandTypes.LINENO],
                                          backpatch=self.semantic_stack[-1][0])
        self.output[self.semantic_stack[-1][0]] = generated_3ac
        del self.semantic_stack[-2:]

        # Save space for uc jump to after else if jpf was not taken
        self.backpatch_save()

    def jp(self):
        # backpatch the uc jump to after else if the first cond was true
        generated_3ac = self.generate_3ac(ThreeAddressCodes.JP,
                                          [self.output_lineno],
                                          [OperandTypes.LINENO],
                                          backpatch=self.semantic_stack[-1][0])
        self.output[self.semantic_stack[-1][0]] = generated_3ac
        self.semantic_stack.pop()

    def enter_while(self):
        # Save lineno for uc jump back after a iteration of the loop
        self.semantic_stack.append([self.output_lineno, OperandTypes.LINENO])

        # Save continue jump target to a separate variable
        # Kind of a hacky and stupid way of doing this but whatever
        self.continue_jump_target.append(self.output_lineno)

    def brk(self):
        self.output.append(None)
        self.break_counter.append([self.output_lineno, OperandTypes.LINENO])
        self.output_lineno += 1

    def cont(self):
        # Jump back to the start of the loop
        if len(self.continue_jump_target) > 0:
            generated_3ac = self.generate_3ac(ThreeAddressCodes.JP,
                                              [self.continue_jump_target[-1]],
                                              [OperandTypes.LINENO])
            self.output.append(generated_3ac)
            self.output_lineno += 1

    def exit_while(self):
        # Backpatch breaks
        while len(self.break_counter) > 0:
            generated_3ac = self.generate_3ac(ThreeAddressCodes.JP,
                                              [self.output_lineno + 1],
                                              [OperandTypes.LINENO],
                                              self.break_counter[-1][0])
            self.output[self.break_counter[-1][0]] = generated_3ac
            self.break_counter.pop()

        # Backpatch the conditional jump over the while
        generated_3ac = self.generate_3ac(ThreeAddressCodes.JPF,
                                          [self.semantic_stack[-2][0], self.output_lineno + 1],
                                          [OperandTypes.ADDRESSING, OperandTypes.LINENO],
                                          self.semantic_stack[-1][0])
        self.output[self.semantic_stack[-1][0]] = generated_3ac

        # Jump back to the start of the loop
        generated_3ac = self.generate_3ac(ThreeAddressCodes.JP,
                                          [self.semantic_stack[-3][0]],
                                          [OperandTypes.LINENO])
        self.output.append(generated_3ac)

        self.output_lineno += 1
        del self.semantic_stack[-3:]

        # Clear continue jump target
        self.continue_jump_target.pop()

    def enter_switch_case(self):
        self.first_case_next.append(True)

    def switch(self):
        generated_3ac = self.generate_3ac(ThreeAddressCodes.ASSIGN,
                                          [self.semantic_stack[-1][0], self.next_temp_addr],
                                          [self.semantic_stack[-1][1], OperandTypes.ADDRESSING])
        self.output.append(generated_3ac)
        self.output_lineno += 1
        self.semantic_stack.pop()
        self.semantic_stack.append([self.next_temp_addr, OperandTypes.ADDRESSING])
        self.increment_temp_addr()

    def save_case(self):
        if not self.first_case_next[-1]:
            generated_3ac = self.generate_3ac(ThreeAddressCodes.JPF,
                                              [self.semantic_stack[-3][0], self.output_lineno],
                                              [self.semantic_stack[-3][1], OperandTypes.LINENO],
                                              self.semantic_stack[-2][0])
            self.output[self.semantic_stack[-2][0]] = generated_3ac
            del self.semantic_stack[-3:-1]

        self.first_case_next[-1] = False

        # Case to match is at the head - 1 of ss
        generated_3ac = self.generate_3ac(ThreeAddressCodes.EQ,
                                          [self.semantic_stack[-1][0], self.semantic_stack[-2][0], self.next_temp_addr],
                                          [
                                              self.semantic_stack[-1][1],
                                              self.semantic_stack[-2][1],
                                              OperandTypes.ADDRESSING
                                          ])
        self.output.append(generated_3ac)
        self.output_lineno += 1
        self.semantic_stack.pop()
        self.semantic_stack.append([self.next_temp_addr, OperandTypes.ADDRESSING])
        self.increment_temp_addr()

        # Save space for conditional jump over the case
        self.backpatch_save()

    def default_case(self):
        generated_3ac = self.generate_3ac(ThreeAddressCodes.JPF,
                                          [self.semantic_stack[-2][0], self.output_lineno],
                                          [self.semantic_stack[-2][1], OperandTypes.LINENO],
                                          self.semantic_stack[-1][0])
        self.output[self.semantic_stack[-1][0]] = generated_3ac
        del self.semantic_stack[-2:]

        self.first_case_next[-1] = False

    def exit_switch_case(self):
        # Backpatch breaks
        while len(self.break_counter) > 0:
            generated_3ac = self.generate_3ac(ThreeAddressCodes.JP,
                                              [self.output_lineno],
                                              [OperandTypes.LINENO],
                                              self.break_counter[-1][0])
            self.output[self.break_counter[-1][0]] = generated_3ac
            self.break_counter.pop()

        self.first_case_next.pop()
        self.semantic_stack.pop()

    def function_called(self):
        if self.function_call_stack[-1] != "output":
            # Copy the parameters
            params = self.function_params[self.function_call_stack[-1]]
            if len(params) > 0:
                given_params = self.semantic_stack[-len(params):]
                for i, param in enumerate(params):
                    if param[2] not in [SymbolType.ARRAY_INT, SymbolType.ARRAY_VOID]:
                        generated_3ac = self.generate_3ac(ThreeAddressCodes.ASSIGN,
                                                          [given_params[i][0], param[1]],
                                                          [given_params[i][1], OperandTypes.ADDRESSING])
                    else:
                        # Assign the address of the array into the variable
                        generated_3ac = self.generate_3ac(ThreeAddressCodes.ASSIGN,
                                                          [given_params[i][0], param[1]],
                                                          [OperandTypes.IMMEDIATE, OperandTypes.ADDRESSING])
                    self.output.append(generated_3ac)
                    self.output_lineno += 1

            del self.semantic_stack[-len(params):]

            # Put the return lineno into the temp that holds the return addr for the called function
            ret_addr_temp = self.function_returns[self.function_call_stack[-1]][0][2]
            generated_3ac = self.generate_3ac(ThreeAddressCodes.ASSIGN,
                                              [self.output_lineno + 2, ret_addr_temp],
                                              [OperandTypes.IMMEDIATE, OperandTypes.ADDRESSING])
            self.output.append(generated_3ac)
            self.output_lineno += 1

            # Jump to called function
            generated_3ac = self.generate_3ac(ThreeAddressCodes.JP,
                                              [self.function_linenos[self.function_call_stack[-1]]],
                                              [OperandTypes.LINENO])
            self.output.append(generated_3ac)
            self.output_lineno += 1

            if self.function_returns[self.function_call_stack[-1]][0][0] is not None:
                # It was not an empty return
                # Assign value from the return address into a new temp
                generated_3ac = self.generate_3ac(ThreeAddressCodes.ASSIGN,
                                                  [
                                                      self.function_returns[self.function_call_stack[-1]][0][0],
                                                      self.next_temp_addr
                                                  ],
                                                  [OperandTypes.ADDRESSING, OperandTypes.ADDRESSING])
                self.output.append(generated_3ac)
                self.output_lineno += 1

                # Get the address into the ss
                self.semantic_stack.append(
                        [self.next_temp_addr, OperandTypes.ADDRESSING]
                )
                self.increment_temp_addr()

            self.function_call_stack.pop()
        else:
            # output was called generate the PRINT
            generated_3ac = self.generate_3ac(ThreeAddressCodes.PRINT,
                                              [self.semantic_stack[-1][0]],
                                              [self.semantic_stack[-1][1]])
            self.output.append(generated_3ac)
            self.output_lineno += 1
            self.semantic_stack.pop()

    def empty_ret(self):
        self.empty_ret_flag = True

    def ret(self):
        if self.current_function[-1] != "main":
            # Store return value and linenumber here for later use if this function get called
            addr_before_increment = self.next_temp_addr
            if self.current_function[-1] not in self.function_returns.keys():
                self.increment_temp_addr()
                self.function_returns[self.current_function[-1]] = (
                    [[addr_before_increment, self.output_lineno + 1, self.next_temp_addr]]
                )
                self.increment_temp_addr()

            # Assign return value into the reserved temp
            if not self.empty_ret_flag:
                generated_3ac = self.generate_3ac(ThreeAddressCodes.ASSIGN,
                                                  [
                                                      self.semantic_stack[-1][0],
                                                      self.function_returns[self.current_function[-1]][0][0]
                                                  ],
                                                  [self.semantic_stack[-1][1], OperandTypes.ADDRESSING])
                self.output.append(generated_3ac)
                self.output_lineno += 1
                self.semantic_stack.pop()
            else:
                self.function_returns[self.current_function[-1]][0][0] = None

            # Jump back to previous function
            generated_3ac = self.generate_3ac(ThreeAddressCodes.JP,
                                              [self.function_returns[self.current_function[-1]][0][2]],
                                              [OperandTypes.INDIRECT_ADDRESSING])
            self.output.append(generated_3ac)
            self.output_lineno += 1

        self.empty_ret_flag = False

    def semantic_actions(self, action_symbol, input_ptr):
        if action_symbol == "#START":
            self.start()
        elif action_symbol == "#END":
            self.end()
        elif action_symbol == "#VARIABLE":
            self.variable()
        elif action_symbol == "#FUNCTION":
            self.function()
        elif action_symbol == "#STATEMENTS_BEGIN":
            self.statements_begin()
        elif action_symbol == "#ENDSCOPE":
            self.end_scope()
        elif action_symbol == "#STOP_PARAM_COUNTER":
            self.stop_param_counter()
        elif action_symbol == "#ARRAY_SIZE":
            self.array_size(input_ptr)
        elif action_symbol == "#PID":
            self.pid(input_ptr)
        elif action_symbol == "#USE_PID":
            self.use_pid(input_ptr)
        elif action_symbol == "#IMMEDIATE":
            self.immediate(input_ptr)
        elif action_symbol == "#INDEXING_DONE":
            self.indexing_done()
        elif action_symbol == "#ASSIGNMENT_CHAIN":
            self.assignment_chain()
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
        elif action_symbol == "#LT":
            self.lt()
        elif action_symbol == "#EQ":
            self.eq()
        elif action_symbol == "#RELOP":
            self.relop()
        elif action_symbol == "#SAVE":
            self.save()
        elif action_symbol == "#JPF_SAVE":
            self.jpf_save()
        elif action_symbol == "#JP":
            self.jp()
        elif action_symbol == "#ENTER_WHILE":
            self.enter_while()
        elif action_symbol == "#BREAK":
            self.brk()
        elif action_symbol == "#CONTINUE":
            self.cont()
        elif action_symbol == "#EXIT_WHILE":
            self.exit_while()
        elif action_symbol == "#ENTER_SWITCH_CASE":
            self.enter_switch_case()
        elif action_symbol == "#SWITCH":
            self.switch()
        elif action_symbol == "#SAVE_CASE":
            self.save_case()
        elif action_symbol == "#DEFAULT_CASE":
            self.default_case()
        elif action_symbol == "#EXIT_SWITCH_CASE":
            self.exit_switch_case()
        elif action_symbol == "#FUNCTION_CALLED":
            self.function_called()
        elif action_symbol == "#EMPTY_RETURN":
            self.empty_ret()
        elif action_symbol == "#RETURN":
            self.ret()
        else:
            pass

    def write_output_to_file(self):
        with open("output.txt", "w") as f:
            for o in self.output:
                f.write(f"{o}\n")
            f.close()
