"""
Leo Kivikunnas 525925
Jaakko Koskela 526050
"""


class CodeGenerator:
    def __init__(self, symbol_table, scope_stack):
        self.symbol_table = symbol_table
        self.scope_stack = scope_stack

    def semantic_actions(self, action_symbol):
        if action_symbol == "#TEST":
            print("TEST")
        elif action_symbol == "#TEST2":
            print("TEST2")
        else:
            pass
