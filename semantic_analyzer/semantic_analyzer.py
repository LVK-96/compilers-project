"""
Leo Kivikunnas 525925
Jaakko Koskela 526050
"""

from scanner import SymbolType


class SemanticAnalyzer:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.ss = 0
        # Count number of params for functions
        self.param_counter_active = False
        self.param_counter = []
        self.errors = []
        self.scope_stack = []

    def get_symbol_table_head(self):
        return list(self.symbol_table.items())[-1]

    def semantic_actions(self, action_symbol, input_ptr, latest_type, lineno):
        if(action_symbol == "#PID"):
            self.pid(input_ptr, latest_type, lineno)

        elif(action_symbol == "#VARIABLE"):
            self.variable(lineno)

        elif(action_symbol == "#FUNCTION"):
            self.function(lineno)

        elif(action_symbol == "#BEGINSCOPE"):
            #Add function ID to scope stack
            next_index = len(list(self.symbol_table.keys())) #next index - index starts from zero
            self.scope_stack.append(next_index)

        elif(action_symbol == "#ENDSCOPE"):
            scope_begin = self.scope_stack.pop()
            to_be_removed = list(self.symbol_table.keys())[scope_begin:]
            #remove symbols from symbol table until we reach the beginning of the scope
            for key in to_be_removed:
                del self.symbol_table[key]
            

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

        elif(action_symbol == ""):
            pass
        elif(action_symbol == ""):
            pass
        elif(action_symbol == ""):
            pass
        elif(action_symbol == ""):
            pass
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


    #Check that variable type not void
    def variable(self, lineno):
        #input pointer not in id anymore, but it is the most recent addition to symbol table
        current = self.get_symbol_table_head()[0]
        try:
            symbol = self.symbol_table[current]
            if (symbol["type"] == SymbolType.INT):
                #okay
                pass
            elif (symbol["type"] == SymbolType.VOID):
                self.report_error(lineno, f"Illegal type of void for {current}")
                #remove from symbol table
                #del self.symbol_table[current] - 
            else:
                #Variable not declared or not in scope - already reported by #pid
                #remove from symbol table?
                self.report_error(lineno, f"{current} is not defined")

        except KeyError:
            #Variable not declared or not in scope - should never happen
            self.report_error(lineno, f"{current} is not defined")
    

    #Mark symbol as a function
    def function(self, lineno):
        #input pointer not in id anymore, but it is the most recent addition to symbol table
        current = self.get_symbol_table_head()[0]
        try:
            symbol = self.symbol_table[current]
            if (symbol["type"] == SymbolType.INT):
                self.symbol_table[current]["type"] = SymbolType.FUNCTION_INT
            elif (symbol["type"] == SymbolType.VOID):
                self.symbol_table[current]["type"] = SymbolType.FUNCTION_VOID
            else:
                #function return type not declared properly - already reported by pid
                #remove from symbol table
                self.report_error(lineno, f"{current} is not defined")

        except KeyError:
            #Function not declared or not in scope - should never happen
            self.report_error(lineno, f"{current} is not defined")


    #Declare ID types and check scopes
    def pid(self, input_ptr, latest_type, lineno):
        current = input_ptr[1]
        try:
            symbol = self.symbol_table[current]
            if(symbol["type"] == None):
                #ID is being declared
                if latest_type == "int":
                    self.symbol_table[current]["type"] = SymbolType.INT
                elif latest_type == "void":
                    self.symbol_table[current]["type"] = SymbolType.VOID
                else:
                    #ID not declared or not in scope
                    self.report_error(lineno, f"{current}  is not defined")
                    #scanner still adds it to symbol table - remove it
                    del self.symbol_table[current]

            elif(symbol["type"] == SymbolType.INT):
                #ID declared and in scope
                pass
            elif(symbol["type"] == SymbolType.FUNCTION_INT):
                #ID declared and in scope
                pass
            elif(symbol["type"] == SymbolType.FUNCTION_VOID):
                #ID declared and in scope
                pass
            else:
                #Invalid type for ID
                pass

        except KeyError:
            #ID not declared or not in scope - this should never be reached
            self.report_error(lineno, f"{current} is not defined")