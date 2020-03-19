"""
Leo Kivikunnas 525925
Jaakko Koskela 526050
"""

from scanner import format_type, SymbolType


class SemanticAnalyzer:
    def __init__(self, symbol_table, scope_stack):
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
        self.scope_stack = scope_stack

        # Store type to check
        # Are we in a while loop
        # Integer represents number of nested loops
        self.in_while = 0

        # Are we in a switch case
        # Integer represents number of nested switch case statements
        self.in_switch_case = 0

        self.type_check_active = False
        self.type_to_check = None

    def get_index(self, name, upper_limit=None, wanted_type=None):
        if upper_limit:
            r = min(upper_limit, len(self.symbol_table))
        else:
            r = len(self.symbol_table)

        wanted_types = []
        if wanted_type == "variable":
            wanted_types = wanted_types + [SymbolType.INT, SymbolType.VOID, SymbolType.ARRAY_INT]
        if wanted_type == "function":
            wanted_types = wanted_types + [SymbolType.FUNCTION_INT, SymbolType.FUNCTION_VOID]

        for i in reversed(range(r)):
            if (
                wanted_type
                and self.symbol_table[i]["name"] == name
                and self.symbol_table[i]["type"] in wanted_types
            ):
                return i
            elif (
                len(wanted_types) == 0
                and self.symbol_table[i]["name"] == name
            ):
                return i

        return None

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
        if self.param_counter_active:
            for i, item in enumerate(self.symbol_table[::-1]):
                if item["type"] in [
                        SymbolType.FUNCTION_VOID,
                        SymbolType.FUNCTION_INT]:
                    self.symbol_table[len(self.symbol_table) - 1 - i]["params"] = self.param_counter
                    break
            self.param_counter = []
            self.param_counter_active = False

    def param(self, latest_type):
        if self.param_counter_active:
            self.param_counter.append(latest_type)

    def array_param(self, latest_type):
        if self.param_counter_active:
            if latest_type == SymbolType.INT:
                self.param_counter.append(SymbolType.ARRAY_INT)
            elif latest_type == SymbolType.VOID:
                self.param_counter.append(SymbolType.ARRAY_VOID)
            else:
                self.param_counter.append(None)

    def start_argument_counter(self, input_ptr):
        idx = self.get_index(input_ptr[1], wanted_type="function")
        if idx is not None and self.symbol_table[idx]["type"] in [SymbolType.FUNCTION_VOID, SymbolType.FUNCTION_INT]:
            # found a function definition
            self.argument_counter_active = True
            self.function_call_stack.append(input_ptr[1])
            self.argument_counter.append([])

    def stop_argument_counter(self, lineno):
        if self.argument_counter_active:
            func_name = self.function_call_stack.pop() if len(
                self.function_call_stack) > 0 else None
            given_args = self.argument_counter.pop() if len(
                self.argument_counter) > 0 else None

            if len(self.argument_counter) == 0 and len(self.function_call_stack) == 0:
                self.argument_counter_active = False

            idx = self.get_index(func_name, wanted_type="function")
            if idx is not None:
                func_params = self.symbol_table[idx]["params"]
                n_of_params = len(func_params)
                if n_of_params != len(given_args):
                    msg = f"Mismatch in numbers of arguments of '{func_name}'."
                    self.report_error(lineno, msg)

                for i, arg in enumerate(given_args):
                    if i >= n_of_params:
                        break

                    expected_type = func_params[i]
                    actual_type = SymbolType.INT if arg[0] == 'NUM' else self.symbol_table[self.get_index(
                        arg[1])]["type"]
                    if not self.compare_types(expected_type, actual_type):
                        expected_type = format_type(expected_type)
                        actual_type = format_type(actual_type)
                        msg = (
                            f"Mismatch in type of argument {i + 1} of '{func_name}'. "
                            f"Expected '{expected_type}' but "
                            f"got '{actual_type}' instead."
                        )
                        self.report_error(lineno, msg)
            else:
                # Function not found from table
                self.report_error(lineno, f"'{func_name}' is not defined.")

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
        idx = self.get_index(input_ptr[1])
        if idx is not None:
            self.type_to_check = self.symbol_table[idx]["type"]
            self.type_check_active = True
        else:
            self.type_to_check = None
            self.type_check_active = False

    def cancel_type_check(self):
        self.type_to_check = None
        self.type_check_active = False

    def type_check(self, lineno, input_ptr):
        if self.type_check_active:
            input_type = None
            if input_ptr[0] == "ID":
                idx = self.get_index(input_ptr[1])
                if idx is not None:
                    input_type = self.symbol_table[idx]["type"]
                else:
                    self.report_error(lineno, f"'{input_ptr[1]}' is not defined.")

            elif input_ptr[0] == "NUM":
                input_type = SymbolType.INT

            if input_type and not self.compare_types(self.type_to_check, input_type):
                input_type = format_type(input_type)
                expected_type = format_type(self.type_to_check)
                msg = (
                    f"Type mismatch in operands, Got {input_type} "
                    f"instead of {expected_type}."
                )
                self.report_error(lineno, msg)

            self.cancel_type_check()

    # Check that variable type not void
    def variable(self, lineno):
        # input pointer not in id anymore, but it is the most recent addition
        # to symbol table
        if self.symbol_table[-1]["type"] != SymbolType.INT:
            # int is the only legal type
            self.report_error(
                lineno,
                (
                    f"Illegal type of {format_type(self.symbol_table[-1]['type'])} "
                    f"for '{self.symbol_table[-1]['name']}'."
                )
            )

    # Mark symbol as a function
    def function(self, lineno):
        # input pointer not in id anymore, but it is the most recent addition
        # to symbol table
        if (self.symbol_table[-1]["type"] == SymbolType.INT):
            self.symbol_table[-1]["type"] = SymbolType.FUNCTION_INT
        elif (self.symbol_table[-1]["type"] == SymbolType.VOID):
            self.symbol_table[-1]["type"] = SymbolType.FUNCTION_VOID
        else:
            # function return type not declared properly - already reported by pid
            self.symbol_table[-1]["type"] = None

    def array(self, lineno):
        if (self.symbol_table[-1]["type"] == SymbolType.INT):
            self.symbol_table[-1]["type"] = SymbolType.ARRAY_INT
        elif (self.symbol_table[-1]["type"] == SymbolType.VOID):
            self.symbol_table[-1]["type"] = SymbolType.ARRAY_VOID
        else:
            self.symbol_table[-1]["type"] = None

    def pid(self, input_ptr, latest_type, lineno):
        current = input_ptr[1]
        idx = self.get_index(current)
        if idx is not None:
            symbol = self.symbol_table[idx]
            if(symbol["type"] is None):
                # ID is being declared
                if latest_type == SymbolType.INT:
                    self.symbol_table[self.get_index(
                        current)]["type"] = SymbolType.INT
                elif latest_type == SymbolType.VOID:
                    self.symbol_table[self.get_index(
                        current)]["type"] = SymbolType.VOID
        else:
            # ID not declared or not in scope - this should never be reached
            self.report_error(lineno, f"'{current}' is not defined.")

    def use_pid(self, input_ptr, lineno):
        current = input_ptr[1]
        idx = self.get_index(current, upper_limit=self.scope_stack[-1])
        if idx is not None:
            # Found in upper scope -> scanner added a false entry
            # Pop false entry added by scanner
            table_entry = self.symbol_table[idx]
            self.symbol_table.pop()

        if idx is None:
            # Not found in upper scope, search local scope
            idx = self.get_index(current)
            table_entry = self.symbol_table[idx]

        if not table_entry["type"] and idx is not None:
            if current != "output":
                self.report_error(lineno, f"'{current}' is not defined.")
                del self.symbol_table[idx]

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
        if action_symbol == "#USE_PID":
            self.use_pid(input_ptr, lineno)
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
