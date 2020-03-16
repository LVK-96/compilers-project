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
        self.param_counter = []
        # Track function calls and arguments given to functions
        # Append new function and
        # new list of arguments when #START_ARGUMENT_COUNTER is ran
        # and input ptr points to function name
        # Head is the active function
        # Pop head in #STOP_ARGUMENT_COUNTER
        self.function_call_stack = []
        self.argument_counter = []
        self.errors = []
        # Are we in a while loop
        # Integer represents number of nested loops
        self.in_while = 0
        # Are we in a switch case
        # Integer represents number of nested switch case statements
        self.in_switch_case = 0

    def get_symbol_table_head(self):
        return list(self.symbol_table.items())[-1]

    def semantic_actions(self, action_symbol, input_ptr, latest_type, lineno):
        if(action_symbol == "#PID"):
            self.pid()
        elif(action_symbol == "#ADD"):
            pass
        elif(action_symbol == "#MULT"):
            pass
        elif(action_symbol == "#ASSIGN"):
            pass

        elif(action_symbol == "#FUNCTION"):
            head = self.get_symbol_table_head()
            if latest_type == "void":
                self.symbol_table[head[0]]["type"] = SymbolType.FUNCTION_VOID
            elif latest_type == "int":
                self.symbol_table[head[0]]["type"] = SymbolType.FUNCTION_INT

        elif(action_symbol == "#END"):
            # Each program must have a main function
            main_found = False
            for key, item in self.symbol_table.items():
                if key == "main" and item["type"] == SymbolType.FUNCTION_VOID and item["params"] == [
                        "void"]:
                    main_found = True
                    break

            if not main_found:
                self.report_error(lineno, "main function not found")

        elif(action_symbol == "#START_PARAM_COUNTER"):
            self.param_counter = []

        elif(action_symbol == "#STOP_PARAM_COUNTER"):
            latest_func = None
            for key, item in self.symbol_table.items():
                if item["type"] in [
                        SymbolType.FUNCTION_VOID,
                        SymbolType.FUNCTION_INT]:
                    latest_func = key

            if latest_func:
                self.symbol_table[latest_func]["params"] = self.param_counter

        elif(action_symbol == "#PARAM"):
            self.param_counter.append(latest_type)

        elif(action_symbol == "#START_ARGUMENT_COUNTER"):
            if self.symbol_table[input_ptr[1]]["type"] in [
                    SymbolType.FUNCTION_VOID, SymbolType.FUNCTION_INT]:
                self.function_call_stack.append(input_ptr[1])
                self.argument_counter.append([])

        elif(action_symbol == "#STOP_ARGUMENT_COUNTER"):
            func_name = self.function_call_stack.pop() if len(
                self.function_call_stack) > 0 else None
            given_args = self.argument_counter.pop() if len(
                self.argument_counter) > 0 else None
            if (len(self.symbol_table[func_name]
                    ["params"]) != len(given_args)):
                self.report_error(
                    lineno, f"Missmatch in number of arguments of '{func_name}'")

        elif(action_symbol == "#ARGUMENT"):
            self.argument_counter[-1].append(input_ptr)

        elif action_symbol == "#WHILE":
            self.in_while += 1

        elif action_symbol == "#EXIT_WHILE":
            self.in_while = max(0, self.in_while - 1)

        elif action_symbol == "#SWITCH_CASE":
            self.in_switch_case += 1

        elif action_symbol == "#EXIT_SWITCH_CASE":
            self.in_switch_case = max(0, self.in_while - 1)

        elif action_symbol == "#CONTINUE":
            if self.in_while == 0:
                msg = "No 'while' found for 'continue'"
                self.report_error(lineno, msg)

        elif action_symbol == "#BREAK":
            if self.in_while == 0 and self.in_switch_case == 0:
                msg = "No 'while' found for 'break'"
                self.report_error(lineno, msg)

        else:
            pass

    def report_error(self, lineno, msg):
        error_msg = f"#{lineno} : Semantic Error! {msg}"
        self.errors.append(error_msg)

    def write_errors_to_file(self):
        with open("semantic_errors.txt", "w") as f:
            if len(self.errors) > 0:
                for i, error in enumerate(self.errors):
                    f.write(f"{error}\n")
            else:
                f.write("There is no semantic errors.")

            f.close()

    def pid(self):
        # query current input from parser
        id = getaddr()
        # check that next input actuallly is a valid type for id?
        self.parser.current_input = getaddr()
        # check that variable declared - within scope
        # get the type from symbol table
        # check that next input actuallly is a valid type for id?
        self.ss.append(next_id)

    def add(self):
        # can be num or id
        first = self.ss.pop()
        second = self.ss.pop()
        # stack should not be empty
        # check both types
        # perform addition
        # create token and push to stack
        result = first + second

    def assign(self):
        pass

    def jpf(self):
        pass

    def jp(self):
        pass

    def save(self):
        pass

    def save_jpf(self):
        pass

    # def get_three_adress(self):
    #    # returns the three address code
    #    pass
