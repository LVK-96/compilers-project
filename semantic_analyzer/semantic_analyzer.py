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

    def get_symbol_table_head(self):
        return list(self.symbol_table.items())[-1]

    def semantic_actions(self, action_symbol, latest_type, lineno):
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
