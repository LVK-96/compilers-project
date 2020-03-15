"""
Leo Kivikunnas 525925
Jaakko Koskela 526050
"""

import weakref


class SemanticAnalyzer:
    def __init__(self, parser):
        self.parser = weakref.ref(parser)
        self.ss = 0
        self.i = 0 # index to address table
        self.three_address_codes = []

    def semantic_actions(self, action_symbol):
        pass
    def pid(self, id):
        #should id be the token for type mismatch checks etc
        #get the address from the table and push that - how to do type checks
        # push token now and get addresses later when you generate the three address code - after type checking!
        self.ss.append()

    def add(self):
        first = ss.pop() #what types are these?
        second = ss.pop()
        result = first + second
        #get temp
        #type check here

    def mult(self):
        pass

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
        #returns the three address code
        pass
