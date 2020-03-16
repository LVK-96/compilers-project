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
                if key == "main" and item["type"] == SymbolType.FUNCTION_VOID: #does it have to be void?
                    main_found = True
                    break

            if not main_found:
                print("Error: void main function not found")

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
        else:
            pass

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

    # def get_three_adress(self):
    #    # returns the three address code
    #    pass
