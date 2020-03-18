"""
Leo Kivikunnas 525925
Jaakko Koskela 526050
"""

from scanner import SymbolType


class SemanticAnalyzer:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.ss = 0
        # Count params for functions in definitions
        self.param_counter_active = False
        self.param_counter = []

        # Track function calls and arguments given to functions
        # Append new function and
        # new list of arguments when #START_ARGUMENT_COUNTER is ran
        # and input ptr points to function name
        # Head is the active function
        # Pop head in #STOP_ARGUMENT_COUNTER
        self.argument_counter_active = False
        self.function_call_stack = []
        self.argument_counter = []
        self.errors = []
        self.scope_stack = []

        # Store type to check
        # Are we in a while loop
        # Integer represents number of nested loops
        self.in_while = 0

        # Are we in a switch case
        # Integer represents number of nested switch case statements
        self.in_switch_case = 0

        self.type_check_active = False
        self.type_to_check = None

    def get_index(self, name):
        for i in reversed(range(len(self.symbol_table))):
            if self.symbol_table[i]["name"] == name:
                return i

    def get_var_index(self, name):
        for i in reversed(range(len(self.symbol_table))):
            if (
                self.symbol_table[i]["name"] == name
                and self.symbol_table[i]["type"] in [SymbolType.INT, SymbolType.VOID, SymbolType.ARRAY_INT]
            ):
                return i

    def get_function_index(self, name):
        for i in reversed(range(len(self.symbol_table))):
            if (
                self.symbol_table[i]["name"] == name
                and self.symbol_table[i]["type"] in [SymbolType.FUNCTION_INT, SymbolType.FUNCTION_VOID]
            ):
                return i

    def compare_types(self, a, b):
        if a == b:
            return True
        elif (
            (a == SymbolType.FUNCTION_INT and b == SymbolType.INT)
            or (a == SymbolType.INT and b == SymbolType.FUNCTION_INT)
        ):
            return True
        elif (
            (a == SymbolType.FUNCTION_VOID and b == SymbolType.VOID)
            or (a == SymbolType.VOID and b == SymbolType.FUNCTION_VOID)
        ):
            return True
        else:
            return False

    def get_symbol_table_head(self):
        return self.symbol_table[-1]

    def report_error(self, lineno, msg):
        error_msg = f"#{lineno} : Semantic Error! {msg}"
        self.errors.append(error_msg)

    def end(self, lineno):
        # Each program must have a main function
        main_found = False
        for item in self.symbol_table:
            if (
                item["name"] == "main"
                and item["type"] == SymbolType.FUNCTION_VOID
                and item["params"] == []
            ):
                main_found = True
                break

        if not main_found:
            self.report_error(lineno, "main function not found!")

    def start_param_counter(self):
        self.param_counter_active = True
        self.param_counter = []

    def stop_param_counter(self):
        latest_func = None
        for item in self.symbol_table[::-1]:
            if item["type"] in [
                    SymbolType.FUNCTION_VOID,
                    SymbolType.FUNCTION_INT]:
                latest_func = item["name"]
                break

        if latest_func:
            self.symbol_table[self.get_function_index(
                latest_func)]["params"] = self.param_counter

        self.param_counter_active = False

    def param(self, latest_type):
        if self.param_counter_active:
            self.param_counter.append(latest_type)

    def array_param(self, latest_type):
        if self.param_counter_active:
            # Just always add array int, array of void is illegal
            # so even if it somewho gets through to this point
            # we still want an array of ints as the type
            self.param_counter.append(SymbolType.ARRAY_INT)

    def start_argument_counter(self, input_ptr):
        try:
            if (
                self.symbol_table[self.get_function_index(input_ptr[1])]["type"]
                in [SymbolType.FUNCTION_VOID, SymbolType.FUNCTION_INT]
            ):
                # found a function definition
                self.argument_counter_active = True;
                self.function_call_stack.append(input_ptr[1])
                self.argument_counter.append([])

        except TypeError:
            # not a function call
            pass

    def stop_argument_counter(self, lineno):
        if self.argument_counter_active:
            func_name = self.function_call_stack.pop() if len(
                self.function_call_stack) > 0 else None
            given_args = self.argument_counter.pop() if len(
                self.argument_counter) > 0 else None

            if len(self.argument_counter) == 0 and len(self.function_call_stack) == 0:
                self.argument_counter_active = False

            if len(self.symbol_table[self.get_function_index(
                    func_name)]["params"]) != len(given_args):
                msg = f"Mismatch in numbers of arguments of '{func_name}'."
                self.report_error(lineno, msg)

            for i, arg in enumerate(given_args):
                if i >= len(
                        self.symbol_table[self.get_function_index(func_name)]["params"]):
                    break
                expected_type = self.symbol_table[self.get_function_index(
                    func_name)]["params"][i]

                actual_type = SymbolType.INT if arg[0] == 'NUM' else self.symbol_table[self.get_var_index(arg[1])]["type"]
                if not self.compare_types(expected_type, actual_type):
                    msg = (
                        f"Mismatch in type of argument {i + 1} for {func_name}. "
                        f"Expected '{expected_type}' but "
                        f"got '{actual_type}' instead'"
                    )
                    self.report_error(lineno, msg)

    def argument(self, input_ptr):
        if self.argument_counter_active:
            self.argument_counter[-1].append(input_ptr)

    def enter_while(self):
        self.in_while += 1

    def exit_while(self):
        self.in_while = max(0, self.in_while - 1)

    def enter_switch_case(self):
        self.in_switch_case += 1

    def exit_switch_case(self):
        self.in_switch_case = max(0, self.in_while - 1)

    def cont(self, lineno):
        if self.in_while == 0:
            msg = "No 'while' found for 'continue'"
            self.report_error(lineno, msg)

    def brk(self, lineno):
        if self.in_while == 0 and self.in_switch_case == 0:
            msg = "No 'while' or 'switch' found for 'break'."
            self.report_error(lineno, msg)

    def start_type_check(self, input_ptr):
        try:
            self.type_to_check = self.symbol_table[self.get_index(
                input_ptr[1])]["type"]
            self.type_check_active = True
        except TypeError:
            self.type_to_check = None
            self.type_check_active = False

    def cancel_type_check(self):
        self.type_to_check = None
        self.type_check_active = False

    def type_check(self, lineno, input_ptr):
        if self.type_check_active:
            input_type = None
            if input_ptr[0] == "ID":
                input_type = self.symbol_table[self.get_index(
                    input_ptr[1])]["type"]
            elif input_ptr[0] == "NUM":
                input_type = SymbolType.INT

            if not self.compare_types(self.type_to_check, input_type):
                if input_type in [
                        SymbolType.FUNCTION_INT,
                        SymbolType.FUNCTION_VOID]:
                    input_type = (
                        SymbolType.INT if input_type == SymbolType.FUNCTION_INT
                        else SymbolType.VOID
                    )
                msg = (
                    f"Type mismatch in operands, Got '{input_type}' "
                    f"instead of '{self.type_to_check}'"
                )
                self.report_error(lineno, msg)

            self.cancel_type_check()

    # Check that variable type not void
    def variable(self, lineno):
        # input pointer not in id anymore, but it is the most recent addition
        # to symbol table
        current = self.get_symbol_table_head()["name"]
        try:
            symbol = self.symbol_table[self.get_var_index(current)]
            if (symbol["type"] == SymbolType.INT):
                # okay
                pass
            elif (symbol["type"] == SymbolType.VOID):
                self.report_error(
                    lineno, f"Illegal type of void for '{current}'.")
                # remove from symbol table
                del self.symbol_table[self.get_var_index(current)]
            else:
                # Variable not declared or not in scope - already reported by #pid
                # remove from symbol table?
                self.report_error(lineno, f"{current} is not defined")

        except KeyError:
            # Variable not declared or not in scope - should never happen
            self.report_error(lineno, f"{current} is not defined")

    # Mark symbol as a function
    def function(self, lineno):
        # ToDo: check that there is a valid function and we arent mistaking a variable - is this only for function declarations - what about function calls
        # input pointer not in id anymore, but it is the most recent addition
        # to symbol table
        current = self.get_symbol_table_head()["name"]
        try:
            symbol = self.symbol_table[self.get_index(current)]
            if (symbol["type"] == SymbolType.INT):
                self.symbol_table[self.get_index(
                    current)]["type"] = SymbolType.FUNCTION_INT
            elif (symbol["type"] == SymbolType.VOID):
                self.symbol_table[self.get_index(
                    current)]["type"] = SymbolType.FUNCTION_VOID
            else:
                # function return type not declared properly - already reported by pid
                # remove from symbol table
                self.report_error(lineno, f"{current} is not defined")

        except KeyError:
            # Function not declared or not in scope - should never happen
            self.report_error(lineno, f"{current} is not defined")

    def array(self, lineno):
        current = self.get_symbol_table_head()["name"]
        try:
            symbol = self.symbol_table[self.get_index(current)]
            if (symbol["type"] == SymbolType.INT):
                self.symbol_table[self.get_index(
                    current)]["type"] = SymbolType.ARRAY_INT
            elif (symbol["type"] == SymbolType.VOID):
                self.report_error(
                    lineno, f"Illegal type of void for array '{current}'.")
            else:
                self.report_error(lineno, f"{current} is not defined")

        except KeyError:
            self.report_error(lineno, f"{current} is not defined")

    # Declare ID types and check scopes

    #how to separate function and variable declaration checks
    def pid(self, input_ptr, latest_type, lineno):
        current = input_ptr[1]
        try:
            symbol = self.symbol_table[self.get_index(current)]
            if(symbol["type"] is None):
                # ID is being declared
                if latest_type == SymbolType.INT:
                    self.symbol_table[self.get_index(
                        current)]["type"] = SymbolType.INT
                elif latest_type == SymbolType.VOID:
                    self.symbol_table[self.get_index(
                        current)]["type"] = SymbolType.VOID
                else:
                    # Not declaring, but referencing
                    # scanner still adds a new symbol to the table - remove it
                    try:
                        # ToDo: at this point we don't know whether it is a variable or a function - we can only do a general check - that something with that name exists
                        self.symbol_table[self.get_index(current)]
                    except TypeError:
                        # ID not declared or not in scope
                        if current != "output":
                            self.report_error(lineno, f"{current} is not defined")

        except TypeError:
            # ID not declared or not in scope - this should never be reached
            self.report_error(lineno, f"{current} is not defined")

    def beginscope(self):
        # Add function ID to scope stack
        # next index - index starts from zero
        next_index = len(self.symbol_table)
        self.scope_stack.append(next_index)

    def endscope(self):
        scope_begin = self.scope_stack.pop()
        to_be_removed = self.symbol_table[scope_begin:]
        # remove symbols from symbol table until we reach the beginning of the
        # scope
        for key in to_be_removed:
            self.symbol_table.pop()

    def semantic_actions(self, action_symbol, input_ptr, latest_type, lineno):
        if action_symbol == "#PID":
            self.pid(input_ptr, latest_type, lineno)
        elif action_symbol == "#VARIABLE":
            self.variable(lineno)
        elif action_symbol == "#FUNCTION":
            self.function(lineno)
        elif action_symbol == "#ARRAY":
            self.array(lineno)
        elif action_symbol == "#BEGINSCOPE":
            self.beginscope()
        elif action_symbol == "#ENDSCOPE":
            self.endscope()
        elif action_symbol == "#END":
            self.end(lineno)
        elif action_symbol == "#START_PARAM_COUNTER":
            self.start_param_counter()
        elif action_symbol == "#STOP_PARAM_COUNTER":
            self.stop_param_counter()
        elif action_symbol == "#PARAM":
            self.param(latest_type)
        elif action_symbol == "#ARRAY_PARAM":
            self.array_param(latest_type)
        elif action_symbol == "#START_ARGUMENT_COUNTER":
            self.start_argument_counter(input_ptr)
        elif action_symbol == "#STOP_ARGUMENT_COUNTER":
            self.stop_argument_counter(lineno)
        elif action_symbol == "#ARGUMENT":
            self.argument(input_ptr)
        elif action_symbol == "#ENTER_WHILE":
            self.enter_while()
        elif action_symbol == "#EXIT_WHILE":
            self.exit_while()
        elif action_symbol == "#ENTER_SWITCH_CASE":
            self.enter_switch_case()
        elif action_symbol == "#EXIT_SWITCH_CASE":
            self.exit_switch_case()
        elif action_symbol == "#CONTINUE":
            self.cont(lineno)
        elif action_symbol == "#BREAK":
            self.brk(lineno)
        elif action_symbol == "#START_TYPE_CHECK":
            self.start_type_check(input_ptr)
        elif action_symbol == "#CANCEL_TYPE_CHECK":
            self.cancel_type_check()
        elif action_symbol == "#TYPE_CHECK":
            self.type_check(lineno, input_ptr)
        else:
            pass

    def write_errors_to_file(self):
        with open("semantic_errors.txt", "w") as f:
            if len(self.errors) > 0:
                for i, error in enumerate(self.errors):
                    f.write(f"{error}\n")
            else:
                f.write("The input program is semantically correct.")

            f.close()
