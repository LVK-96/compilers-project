"""
Leo Kivikunnas 525925
Jaakko Koskela 526050
"""

from scanner import SymbolType


class SemanticAnalyzer:
    def __init__(self, symbol_table):
        self.symbol_table = symbol_table
        self.ss = 0
        # self.i = 0  # index to address table
        # self.three_address_codes = []

    def get_symbol_table_head(self):
        return list(self.symbol_table.items())[-1]

    def semantic_actions(self, action_symbol, latest_type):
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
                self.symbol_table[head[0]] = SymbolType.FUNCTION_VOID
            elif latest_type == "int":
                self.symbol_table[head[0]] = SymbolType.FUNCTION_INT
        elif(action_symbol == "#END"):
            # Each program must have a main function
            main_found = False
            for key, type in self.symbol_table.items():
                if key == "main" and type == SymbolType.FUNCTION_VOID:
                    main_found = True
                    break

            if not main_found:
                print("Error: void main function not found")

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
