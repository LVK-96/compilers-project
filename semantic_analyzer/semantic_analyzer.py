"""
Leo Kivikunnas 525925
Jaakko Koskela 526050
"""

import weakref
from parser import get_addr


class SemanticAnalyzer:
    def __init__(self, parser):
        self.parser = weakref.ref(parser)
        self.ss = 0
        # self.i = 0  # index to address table
        #self.three_address_codes = []

    def semantic_actions(self, action_symbol):
        if(action_symbol == "#PID"):
            pass
        elif(action_symbol == "#ADD"):
            pass
        elif(action_symbol == "#MULT"):
            pass
        elif(action_symbol == "#ASSIGN"):
            pass
        elif(action_symbol == ""):
            pass
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
        self.ss.append(next_id)

    def add(self):
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

    def get_three_adress(self):
        # returns the three address code
        pass
