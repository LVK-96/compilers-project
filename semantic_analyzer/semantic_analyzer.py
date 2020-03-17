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

        # Store type to check
        # Are we in a while loop
        # Integer represents number of nested loops
        self.in_while = 0

<<<<<<< HEAD
    def semantic_actions(self, action_symbol, latest_type, lineno):
        if(action_symbol == "#PID"):
            self.pid(latest_type)
        elif(action_symbol == "#ADD"):
            pass
        elif(action_symbol == "#MULT"):
            pass
        elif(action_symbol == "#ASSIGN"):
            pass
        elif(action_symbol == "#FUNCTION"):
            #update scope stack 
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
            self.param_counter_active = True
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

            self.param_counter_active = False

        elif(action_symbol == "#PARAM"):
            if self.param_counter_active:
                self.param_counter.append(latest_type)

        elif(action_symbol == "#ENDFUNCTION"):
            #remove variables from symbol table and pop scope stack
            #Is a generalized action symbol possible eg. #ENDSCOPE 
            pass
        elif(action_symbol == ""):
            pass
        elif(action_symbol == ""):
            pass
        elif(action_symbol == ""):
            pass
=======
        # Are we in a switch case
        # Integer represents number of nested switch case statements
        self.in_switch_case = 0

        self.type_check_active = False
        self.type_to_check = None

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
>>>>>>> 06c0841216a0c6b49ffb2fb80e366f5741221037
        else:
            return False

    def get_symbol_table_head(self):
        return list(self.symbol_table.items())[-1]

    #this is only for ID declarations - no assignment - no push to semantic stack?
    def pid(self, latest_type):
        #update type to symbol table
        head = self.get_symbol_table_head() #the id latest type refers to is the latest addition to symbol table
        if latest_type == "void":
            self.symbol_table[head[0]]["type"] = SymbolType.VOID #okay for functions, but not for other ID:s
        elif latest_type == "int":
            self.symbol_table[head[0]]["type"] = SymbolType.INT
        else:
            #error invalid type for 
            print("Error: Invalid type for ID")

    #checks for declarations and scopes
    def rid(self):
        #check that in symbol table
        #check that type is correct
        #check that in scope
        pass


    def assign(self):
        #what we assign to must be ID and it must have been defined
        #exmpale a = 3; - case for num - a needs to be defined - id with out definition -> check that it is defined
        pass

    def report_error(self, lineno, msg):
        error_msg = f"#{lineno} : Semantic Error! {msg}"
        self.errors.append(error_msg)

    def function(self, latest_type):
        head = self.get_symbol_table_head()
        if latest_type == SymbolType.VOID:
            self.symbol_table[head[0]]["type"] = SymbolType.FUNCTION_VOID
        elif latest_type == SymbolType.INT:
            self.symbol_table[head[0]]["type"] = SymbolType.FUNCTION_INT

    def end(self, lineno):
        # Each program must have a main function
        main_found = False
        for key, item in self.symbol_table.items():
            if (
                key == "main"
                and item["type"] == SymbolType.FUNCTION_VOID
                and item["params"] == []
            ):
                main_found = True
                break

        if not main_found:
            self.report_error(lineno, "main function not found")

    def start_param_counter(self):
        self.param_counter = []

    def stop_param_counter(self):
        latest_func = None
        for key, item in self.symbol_table.items():
            if item["type"] in [
                    SymbolType.FUNCTION_VOID,
                    SymbolType.FUNCTION_INT]:
                latest_func = key

        if latest_func:
            self.symbol_table[latest_func]["params"] = self.param_counter

    def param(self, latest_type):
        self.param_counter.append(latest_type)

    def start_argument_counter(self, input_ptr):
        if (
            self.symbol_table[input_ptr[1]]["type"]
            in [SymbolType.FUNCTION_VOID, SymbolType.FUNCTION_INT]
        ):
            self.function_call_stack.append(input_ptr[1])
            self.argument_counter.append([])

    def stop_argument_counter(self, lineno):
        func_name = self.function_call_stack.pop() if len(
            self.function_call_stack) > 0 else None
        given_args = self.argument_counter.pop() if len(
            self.argument_counter) > 0 else None

        if len(self.symbol_table[func_name]["params"]) != len(given_args):
            msg = f"Missmatch in number of arguments of '{func_name}'"
            self.report_error(lineno, msg)

        for i, arg in enumerate(given_args):
            if i >= len(self.symbol_table[func_name]["params"]):
                break
            expected_type = self.symbol_table[func_name]["params"][i]
            actual_type = self.symbol_table[arg[1]]["type"]
            if not self.compare_types(expected_type, actual_type):
                msg = (
                    f"Mismatch in type of argument {i + 1} for {func_name}. "
                    f"Expected '{expected_type}' but "
                    f"got '{actual_type}' instead'"
                )
                self.report_error(lineno, msg)

    def argument(self, input_ptr):
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
            msg = "No 'while' or 'switch' found for 'break'"
            self.report_error(lineno, msg)

    def start_type_check(self, input_ptr):
        self.type_to_check = self.symbol_table[input_ptr[1]]["type"]
        self.type_check_active = True

    def cancel_type_check(self):
        self.type_to_check = None
        self.type_check_active = False

    def type_check(self, lineno, input_ptr):
        if self.type_check_active:
            input_type = None
            if input_ptr[0] == "ID":
                input_type = self.symbol_table[input_ptr[1]]["type"]
            elif input_ptr[0] == "NUM":
                input_type = SymbolType.INT

            if not self.compare_types(self.type_to_check, input_type):
                if input_type in [SymbolType.FUNCTION_INT, SymbolType.FUNCTION_VOID]:
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


    def add(self):
        # can be num or id
        first = self.ss.pop()
        second = self.ss.pop()
        # stack should not be empty
        # check both types
        # perform addition
        # create token and push to stack
        result = first + second



    def jpf(self):
        pass

    def jp(self):
        pass

    def save(self):
        pass

    def save_jpf(self):
        pass

    def semantic_actions(self, action_symbol, input_ptr, latest_type, lineno):
        if action_symbol == "#PID":
            self.pid()
        elif action_symbol == "#ADD":
            pass
        elif action_symbol == "#MULT":
            pass
        elif action_symbol == "#ASSIGN":
            pass
        elif action_symbol == "#FUNCTION":
            self.function(latest_type)
        elif action_symbol == "#END":
            self.end(lineno)
        elif action_symbol == "#START_PARAM_COUNTER":
            self.start_param_counter()
        elif action_symbol == "#STOP_PARAM_COUNTER":
            self.stop_param_counter()
        elif action_symbol == "#PARAM":
            self.param(latest_type)
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
                f.write("There is no semantic errors.")

            f.close()

    # def get_three_adress(self):
    #    # returns the three address code
    #    pass
