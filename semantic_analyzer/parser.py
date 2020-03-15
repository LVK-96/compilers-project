"""
leo kivikunnas 525925
jaakko koskela 526050
"""

from scanner import Scanner
from anytree import Node, RenderTree

symbols = [";", ":", ",", "[", "]", "(", ")", "{", "}",
           "+", "-", "*", "=", "<", "=="]
keywords = ["if", "else", "void", "int", "while", "break",
            "continue", "switch", "default", "case", "return"]

terminals = ["ID", "NUM"] + symbols + keywords + ["$"]

non_terminals = [
    "Program",
    "Declaration-list",
    "Declaration",
    "Declaration-initial",
    "Declaration-prime",
    "Var-declaration-prime",
    "Fun-declaration-prime",
    "Type-specifier",
    "Params",
    "Param-list-void-abtar",
    "Param-list",
    "Param",
    "Param-prime",
    "Compound-stmt",
    "Statement-list",
    "Statement",
    "Expression-stmt",
    "Selection-stmt",
    "Iteration-stmt",
    "Return-stmt",
    "Return-stmt-prime",
    "Switch-stmt",
    "Case-stmts",
    "Case-stmt",
    "Default-stmt",
    "Expression",
    "B",
    "H",
    "Simple-expression-zegond",
    "Simple-expression-prime",
    "C",
    "Relop",
    "Additive-expression",
    "Additive-expression-prime",
    "Additive-expression-zegond",
    "D",
    "Addop",
    "Term",
    "Term-prime",
    "Term-zegond",
    "G",
    "Factor",
    "Var-call-prime",
    "Var-prime",
    "Factor-prime",
    "Factor-zegond",
    "Args",
    "Arg-list",
    "Arg-list-prime"
]

firsts = {
    "Program": ["void", "EPSILON", "int"],
    "Declaration-list": ["void", "EPSILON", "int"],
    "Declaration": ["void", "int"],
    "Declaration-initial": ["void", "int"],
    "Declaration-prime": ["(", "[", ";"],
    "Var-declaration-prime": ["[", ";"],
    "Fun-declaration-prime": ["("],
    "Type-specifier": ["void", "int"],
    "Params": ["void", "int"],
    "Param-list-void-abtar": ["EPSILON", "ID"],
    "Param-list": ["EPSILON", ","],
    "Param": ["void", "int"],
    "Param-prime": ["EPSILON", "["],
    "Compound-stmt": ["{"],
    "Statement-list": ["NUM", "switch", ";", "{", "(", "ID", "EPSILON", "return", "if", "while", "continue", "break"],
    "Statement": ["return", "NUM", "switch", ";", "{", "(", "ID", "continue", "if", "while", "break"],
    "Expression-stmt": ["NUM", ";", "(", "ID", "continue", "break"],
    "Selection-stmt": ["if"], "Iteration-stmt": ["while"],
    "Return-stmt": ["return"],
    "Return-stmt-prime": ["(", "NUM", "ID", ";"],
    "Switch-stmt": ["switch"],
    "Case-stmts": ["case", "EPSILON"],
    "Case-stmt": ["case"],
    "Default-stmt": ["EPSILON", "default"],
    "Expression": ["(", "NUM", "ID"],
    "B": ["*", "-", "==", "<", "+", "=", "(", "EPSILON", "["],
    "H": ["*", "-", "==", "<", "+", "=", "EPSILON"],
    "Simple-expression-zegond": ["(", "NUM"],
    "Simple-expression-prime": ["*", "-", "==", "<", "+", "(", "EPSILON"],
    "C": ["==", "<", "EPSILON"],
    "Relop": ["==", "<"],
    "Additive-expression": ["(", "NUM", "ID"],
    "Additive-expression-prime": ["*", "-", "+", "(", "EPSILON"],
    "Additive-expression-zegond": ["(", "NUM"],
    "D": ["-", "EPSILON", "+"],
    "Addop": ["-", "+"],
    "Term": ["(", "NUM", "ID"],
    "Term-prime": ["(", "EPSILON", "*"],
    "Term-zegond": ["(", "NUM"],
    "G": ["EPSILON", "*"],
    "Factor": ["(", "NUM", "ID"],
    "Var-call-prime": ["(", "EPSILON", "["],
    "Var-prime": ["EPSILON", "["],
    "Factor-prime": ["(", "EPSILON"],
    "Factor-zegond": ["(", "NUM"],
    "Args": ["(", "EPSILON", "NUM", "ID"],
    "Arg-list": ["(", "NUM", "ID"],
    "Arg-list-prime": ["EPSILON", ","]
}

follows = {
    "Program": ["$"],
    "Declaration-list": ["$", "case", "NUM", "switch", ";", "{", "}", "(", "default", "ID", "return", "if", "while", "continue", "break"],
    "Declaration": ["void", "$", "case", "NUM", "switch", "int", ";", "{", "}", "(", "default", "ID", "return", "if", "while", "continue", "break"],
    "Declaration-initial": [",", ";", "(", "[", ")"],
    "Declaration-prime": ["void", "$", "case", "NUM", "switch", "int", ";", "{", "}", "(", "default", "ID", "return", "if", "while", "continue", "break"],
    "Var-declaration-prime": ["void", "$", "case", "NUM", "switch", "int", ";", "{", "}", "(", "default", "ID", "return", "if", "while", "continue", "break"],
    "Fun-declaration-prime": ["void", "$", "case", "NUM", "switch", "int", ";", "{", "}", "(", "default", "ID", "return", "if", "while", "continue", "break"],
    "Type-specifier": ["ID"],
    "Params": [")"],
    "Param-list-void-abtar": [")"],
    "Param-list": [")"],
    "Param": [",", ")"],
    "Param-prime": [",", ")"],
    "Compound-stmt": ["void", "$", "case", "NUM", "switch", "int", ";", "{", "}", "(", "default", "ID", "return", "if", "while", "else", "continue", "break"],
    "Statement-list": ["case", "default", "}"],
    "Statement": ["case", "NUM", "switch", ";", "{", "}", "(", "default", "ID", "return", "if", "while", "else", "continue", "break"],
    "Expression-stmt": ["case", "NUM", "switch", ";", "{", "}", "(", "default", "ID", "return", "if", "while", "else", "continue", "break"],
    "Selection-stmt": ["case", "NUM", "switch", ";", "{", "}", "(", "default", "ID", "return", "if", "while", "else", "continue", "break"],
    "Iteration-stmt": ["case", "NUM", "switch", ";", "{", "}", "(", "default", "ID", "return", "if", "while", "else", "continue", "break"],
    "Return-stmt": ["case", "NUM", "switch", ";", "{", "}", "(", "default", "ID", "return", "if", "while", "else", "continue", "break"],
    "Return-stmt-prime": ["case", "NUM", "switch", ";", "{", "}", "(", "default", "ID", "return", "if", "while", "else", "continue", "break"],
    "Switch-stmt": ["case", "NUM", "switch", ";", "{", "}", "(", "default", "ID", "return", "if", "while", "else", "continue", "break"],
    "Case-stmts": ["default", "}"],
    "Case-stmt": ["case", "default", "}"],
    "Default-stmt": ["}"],
    "Expression": ["]", ",", ")", ";"],
    "B": ["]", ",", ")", ";"],
    "H": ["]", ",", ")", ";"],
    "Simple-expression-zegond": ["]", ",", ")", ";"],
    "Simple-expression-prime": ["]", ",", ")", ";"],
    "C": ["]", ",", ")", ";"],
    "Relop": ["(", "NUM", "ID"],
    "Additive-expression": ["]", ",", ")", ";"],
    "Additive-expression-prime": ["]", ",", ";", "==", "<", ")"],
    "Additive-expression-zegond": ["]", ",", ";", "==", "<", ")"],
    "D": ["]", ",", ";", "==", "<", ")"],
    "Addop": ["(", "NUM", "ID"],
    "Term": ["]", ",", ";", "-", "<", "==", "+", ")"],
    "Term-prime": ["]", ",", ";", "-", "<", "==", "+", ")"],
    "Term-zegond": ["]", ",", ";", "-", "<", "==", "+", ")"],
    "G": ["]", ",", ";", "-", "<", "==", "+", ")"],
    "Factor": ["]", ",", "*", ";", "-", "<", "==", "+", ")"],
    "Var-call-prime": ["]", ",", "*", ";", "-", "<", "==", "+", ")"],
    "Var-prime": ["]", ",", "*", ";", "-", "<", "==", "+", ")"],
    "Factor-prime": ["]", ",", "*", ";", "-", "<", "==", "+", ")"],
    "Factor-zegond": ["]", ",", "*", ";", "-", "<", "==", "+", ")"],
    "Args": [")"],
    "Arg-list": [")"],
    "Arg-list-prime": [")"]
}

ll1_table = [
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'Declaration-list', 'Declaration-list', None, None, None, None, None, None, None, 'Declaration-list'],
    ['EPSILON', 'EPSILON', 'EPSILON', None, None, None, None, 'EPSILON', None, 'EPSILON', 'EPSILON', None, None, None, None, None, None, 'EPSILON', None, 'Declaration Declaration-list', 'Declaration Declaration-list', 'EPSILON', 'EPSILON', 'EPSILON', 'EPSILON', 'EPSILON', 'EPSILON', 'EPSILON', 'EPSILON'],
    ['SYNCH', 'SYNCH', 'SYNCH', None, None, None, None, 'SYNCH', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, 'SYNCH', None, 'Declaration-initial Declaration-prime', 'Declaration-initial Declaration-prime', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH'],
    [None, None, 'SYNCH', None, 'SYNCH', 'SYNCH', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, None, None, None, None, 'Type-specifier ID', 'Type-specifier ID', None, None, None, None, None, None, None, None],
    ['SYNCH', 'SYNCH', 'Var-declaration-prime', None, None, 'Var-declaration-prime', None, 'Fun-declaration-prime', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, 'SYNCH', None, 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH'],
    ['SYNCH', 'SYNCH', ';', None, None, '[ NUM ] ;', None, 'SYNCH', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, 'SYNCH', None, 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH'],
    ['SYNCH', 'SYNCH', 'SYNCH', None, None, None, None, '( Params ) Compound-stmt', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, 'SYNCH', None, 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH'],
    ['SYNCH', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'void', 'int', None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, 'SYNCH', None, None, None, None, None, None, None, None, None, None, 'void Param-list-void-abtar', 'int ID Param-prime Param-list', None, None, None, None, None, None, None, None],
    ['ID Param-prime Param-list', None, None, None, None, None, None, None, 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, ', Param Param-list', None, None, None, 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, 'SYNCH', None, None, None, 'SYNCH', None, None, None, None, None, None, None, None, None, None, 'Declaration-initial Param-prime', 'Declaration-initial Param-prime', None, None, None, None, None, None, None, None],
    [None, None, None, None, 'EPSILON', '[ ]', None, None, 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    ['SYNCH', 'SYNCH', 'SYNCH', None, None, None, None, 'SYNCH', None, '{ Declaration-list Statement-list }', 'SYNCH', None, None, None, None, None, None, 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH'],
    ['Statement Statement-list', 'Statement Statement-list', 'Statement Statement-list', None, None, None, None, 'Statement Statement-list', None, 'Statement Statement-list', 'EPSILON', None, None, None, None, None, None, 'Statement Statement-list', None, None, None, 'Statement Statement-list', 'Statement Statement-list', 'Statement Statement-list', 'Statement Statement-list', 'EPSILON', 'EPSILON', 'Statement Statement-list', None],
    ['Expression-stmt', 'Expression-stmt', 'Expression-stmt', None, None, None, None, 'Expression-stmt', None, 'Compound-stmt', 'SYNCH', None, None, None, None, None, None, 'Selection-stmt', 'SYNCH', None, None, 'Iteration-stmt', 'Expression-stmt', 'Expression-stmt', 'Switch-stmt', 'SYNCH', 'SYNCH', 'Return-stmt', None],
    ['Expression ;', 'Expression ;', ';', None, None, None, None, 'Expression ;', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, 'SYNCH', 'SYNCH', None, None, 'SYNCH', 'break ;', 'continue ;', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', None],
    ['SYNCH', 'SYNCH', 'SYNCH', None, None, None, None, 'SYNCH', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, 'if ( Expression ) Statement else Statement', 'SYNCH', None, None, 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', None],
    ['SYNCH', 'SYNCH', 'SYNCH', None, None, None, None, 'SYNCH', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, 'SYNCH', 'SYNCH', None, None, 'while ( Expression ) Statement', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', None],
    ['SYNCH', 'SYNCH', 'SYNCH', None, None, None, None, 'SYNCH', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, 'SYNCH', 'SYNCH', None, None, 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'return Return-stmt-prime', None],
    ['Expression ;', 'Expression ;', ';', None, None, None, None, 'Expression ;', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, 'SYNCH', 'SYNCH', None, None, 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', None],
    ['SYNCH', 'SYNCH', 'SYNCH', None, None, None, None, 'SYNCH', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, 'SYNCH', 'SYNCH', None, None, 'SYNCH', 'SYNCH', 'SYNCH', 'switch ( Expression ) { Case-stmts Default-stmt }', 'SYNCH', 'SYNCH', 'SYNCH', None],
    [None, None, None, None, None, None, None, None, None, None, 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'EPSILON', 'Case-stmt Case-stmts', None, None],
    [None, None, None, None, None, None, None, None, None, None, 'SYNCH', None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'SYNCH', 'case NUM : Statement-list', None, None],
    [None, None, None, None, None, None, None, None, None, None, 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'default : Statement-list', None, None, None],
    ['ID B', 'Simple-expression-zegond', 'SYNCH', None, 'SYNCH', None, 'SYNCH', 'Simple-expression-zegond', 'SYNCH', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, 'Simple-expression-prime', None, 'Simple-expression-prime', '[ Expression ] H', 'Simple-expression-prime', 'Simple-expression-prime', 'Simple-expression-prime', None, None, 'Simple-expression-prime', 'Simple-expression-prime', 'Simple-expression-prime', '= Expression', 'Simple-expression-prime', 'Simple-expression-prime', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, 'G D C', None, 'G D C', None, 'G D C', None, 'G D C', None, None, 'G D C', 'G D C', 'G D C', '= Expression', 'G D C', 'G D C', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, 'Additive-expression-zegond C', 'SYNCH', None, 'SYNCH', None, 'SYNCH', 'Additive-expression-zegond C', 'SYNCH', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, 'Additive-expression-prime C', None, 'Additive-expression-prime C', None, 'Additive-expression-prime C', 'Additive-expression-prime C', 'Additive-expression-prime C', None, None, 'Additive-expression-prime C', 'Additive-expression-prime C', 'Additive-expression-prime C', None, 'Additive-expression-prime C', 'Additive-expression-prime C', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, 'EPSILON', None, 'EPSILON', None, 'EPSILON', None, 'EPSILON', None, None, None, None, None, None, 'Relop Additive-expression', 'Relop Additive-expression', None, None, None, None, None, None, None, None, None, None, None, None],
    ['SYNCH', 'SYNCH', None, None, None, None, None, 'SYNCH', None, None, None, None, None, None, None, '<', '==', None, None, None, None, None, None, None, None, None, None, None, None],
    ['Term D', 'Term D', 'SYNCH', None, 'SYNCH', None, 'SYNCH', 'Term D', 'SYNCH', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, 'Term-prime D', None, 'Term-prime D', None, 'Term-prime D', 'Term-prime D', 'Term-prime D', None, None, 'Term-prime D', 'Term-prime D', 'Term-prime D', None, 'Term-prime D', 'Term-prime D', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, 'Term-zegond D', 'SYNCH', None, 'SYNCH', None, 'SYNCH', 'Term-zegond D', 'SYNCH', None, None, None, None, None, None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, 'EPSILON', None, 'EPSILON', None, 'EPSILON', None, 'EPSILON', None, None, 'Addop Term D', 'Addop Term D', None, None, 'EPSILON', 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None],
    ['SYNCH', 'SYNCH', None, None, None, None, None, 'SYNCH', None, None, None, '+', '-', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    ['Factor G', 'Factor G', 'SYNCH', None, 'SYNCH', None, 'SYNCH', 'Factor G', 'SYNCH', None, None, 'SYNCH', 'SYNCH', None, None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, 'Factor-prime G', None, 'Factor-prime G', None, 'Factor-prime G', 'Factor-prime G', 'Factor-prime G', None, None, 'Factor-prime G', 'Factor-prime G', 'Factor-prime G', None, 'Factor-prime G', 'Factor-prime G', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, 'Factor-zegond G', 'SYNCH', None, 'SYNCH', None, 'SYNCH', 'Factor-zegond G', 'SYNCH', None, None, 'SYNCH', 'SYNCH', None, None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, 'EPSILON', None, 'EPSILON', None, 'EPSILON', None, 'EPSILON', None, None, 'EPSILON', 'EPSILON', '* Factor G', None, 'EPSILON', 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None],
    ['ID Var-call-prime', 'NUM', 'SYNCH', None, 'SYNCH', None, 'SYNCH', '( Expression )', 'SYNCH', None, None, 'SYNCH', 'SYNCH', 'SYNCH', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, 'Var-prime', None, 'Var-prime', 'Var-prime', 'Var-prime', '( Args )', 'Var-prime', None, None, 'Var-prime', 'Var-prime', 'Var-prime', None, 'Var-prime', 'Var-prime', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, 'EPSILON', None, 'EPSILON', '[ Expression ]', 'EPSILON', None, 'EPSILON', None, None, 'EPSILON', 'EPSILON', 'EPSILON', None, 'EPSILON', 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, 'EPSILON', None, 'EPSILON', None, 'EPSILON', '( Args )', 'EPSILON', None, None, 'EPSILON', 'EPSILON', 'EPSILON', None, 'EPSILON', 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, 'NUM', 'SYNCH', None, 'SYNCH', None, 'SYNCH', '( Expression )', 'SYNCH', None, None, 'SYNCH', 'SYNCH', 'SYNCH', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, None, None, None, None, None, None],
    ['Arg-list', 'Arg-list', None, None, None, None, None, 'Arg-list', 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    ['Expression Arg-list-prime', 'Expression Arg-list-prime', None, None, None, None, None, 'Expression Arg-list-prime', 'SYNCH', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, ', Expression Arg-list-prime', None, None, None, 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
]


class LL1_parser:
    def __init__(self, table, terminals, non_terminals, data, scanner):
        self.table = table
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.stack = ["$", "Program"]
        self.scanner = scanner
        self.data = data
        self.input_ptr = self.scanner.get_next_token()
        self.tree = Node("Program")
        self.current_node = self.tree
        self.errors = []
        self.lineno = 1

    def remove_node(self, name):
        # Used in error handling to remove all nonterminals of a node
        orig_node = self.current_node
        while True:
            self.current_node = self.current_node.parent
            found = False
            for child in self.current_node.children:
                if not child.children and child.name == name:
                    child.parent = None
                    found = True
                    break
            if found:
                break

        # Reset current node to where it was before
        self.current_node = orig_node

    def report_error(self, lineno, msg):
        error_msg = f"#{lineno} : Syntax Error, {msg}"
        self.errors.append(error_msg)

    def find_simplest_construct(self, popped):
        options = [popped]
        shortest = None
        while not shortest:
            new_options = options.copy()
            for o in options:
                elems = o.split(" ")
                new_elems = elems.copy()
                for elem in elems:
                    if elem in non_terminals:
                        # Expand non terminal
                        i = non_terminals.index(elem)
                        row = ll1_table[i]
                        for rule in row:
                            if rule and rule != "SYNCH":
                                # Use rule
                                i = elems.index(elem)
                                new_elems[i] = rule
                                new_option = " ".join(new_elems)
                                i = options.index(o)
                                if new_option not in new_options:
                                    if new_options[i] == options[i]:
                                        new_options[i] = new_option
                                    else:
                                        new_options.append(new_option)
                        # Only expand one rule per pass
                        break

            options = new_options
            candidates = []
            for o in options:
                elems = o.split(" ")
                # Don't consider epsilons in length
                elems_no_eps = list(filter(("EPSILON").__ne__, elems))
                candidate = True
                for e in elems_no_eps:
                    if e in non_terminals:
                        candidate = False
                        break
                if candidate and len(elems_no_eps) > 0:
                    candidates.append(elems_no_eps)

            if len(candidates) > 0:
                shortest = candidates[0]
                for c in candidates:
                    if len(c) < len(shortest):
                        shortest = c

        return shortest[0]

    def handle_error(self, production, to_compare):
        orig_lineno = self.lineno
        if not production and self.stack[-1] in non_terminals:
            # Empty production
            orig_input_ptr = self.input_ptr
            tmp = self.scanner.get_next_token()
            self.input_ptr = (tmp[0], tmp[1])
            self.lineno = tmp[2]
            if self.input_ptr[1] == "$" and orig_input_ptr[1] == "$":
                # We are at EOF, empty file and stop parsing
                for i in range(1, len(self.stack)):
                    item = self.stack[i]
                    self.remove_node(item)
                self.stack = []  # Empty stack so parsing stops
                self.report_error(orig_lineno + 1, f"Unexpected EndOfFile")
            else:
                self.report_error(
                    orig_lineno, f"illegal {orig_input_ptr[to_compare]}")
        else:
            popped = self.stack.pop()
            if popped in non_terminals:
                # Synch
                self.remove_node(popped)
                self.report_error(
                    orig_lineno,
                    f'missing "{self.find_simplest_construct(popped)}"')
            else:
                # Mismatched terminal at head of stack and input
                if popped != "$":
                    self.report_error(orig_lineno, f'missing "{popped}"')

    def step(self):
        head = self.stack[-1]
        to_compare = 1
        if self.input_ptr[0] == "NUM" or self.input_ptr[0] == "ID":
            to_compare = 0

        if self.input_ptr[to_compare] == head:
            popped = self.stack.pop()
            if(popped != '$'):
                self.add_nodes(popped, [], self.input_ptr)
            tmp = self.scanner.get_next_token()
            self.input_ptr = (tmp[0], tmp[1])
            self.lineno = tmp[2]

        else:
            column = self.terminals.index(self.input_ptr[to_compare])
            row = self.non_terminals.index(
                head) if head in self.non_terminals else None
            production = ll1_table[row][column] if row is not None else None
            if production and production != "SYNCH":
                start = self.stack.pop()
                items = production.split(" ")
                for item in items[::-1]:
                    if (item != "EPSILON"):
                        self.stack.append(item)
                # add nodes to tree
                self.add_nodes(start, items, self.input_ptr)
            else:
                self.handle_error(production, to_compare)

    # start is the lhs o production and items make up the rhs
    def add_nodes(self, start, items, input_ptr):
        # find the start point
        while(self.current_node.name != start):
            # move up
            self.current_node = self.current_node.parent
            # check children for start
            for child in self.current_node.children:
                if child.name == start and not child.children:
                    # start found move there
                    self.current_node = child
                    break

        left_node = None

        for item in items:
            left_node = Node(item, parent=self.current_node)

        if self.current_node.name in ["ID", "NUM"]:
            self.current_node.name = f"({input_ptr[0]}, {input_ptr[1]})"

        if self.current_node.name in symbols:
            self.current_node.name = f"(SYMBOL, {self.current_node.name})"

        if self.current_node.name in keywords:
            self.current_node.name = f"(KEYWORD, {self.current_node.name})"

        # move to leftmost node
        if(left_node):
            self.current_node = left_node

    def write_tree_to_file(self):
        with open("parse_tree.txt", "w") as f:
            for pre, _, node in RenderTree(self.tree.root):
                print("%s%s" % (pre, node.name), file=f)

    def print_tree(self):
        for pre, _, node in RenderTree(self.tree.root):
            print("%s%s" % (pre, node.name))

    def write_errors_to_file(self):
        with open("syntax_errors.txt", "w") as f:
            if len(self.errors) > 0:
                for error in self.errors:
                    f.write(f"{error}\n")
            else:
                f.write("There is no syntax error.")

            f.close()

def get_addr():
    #placeholder for getting the current input token for semantic analysis
    return ("ID", 1)

def main():
    filename = "input.txt"
    with open(filename) as f:
        data = f.read()
        data = data.rstrip("\n")
        f.close()

    scanner = Scanner(filename, symbols, keywords, data)
    parser = LL1_parser(
        ll1_table,
        terminals,
        non_terminals,
        data,
        scanner
    )
    while True:
        parser.step()
        if (len(parser.stack) < 1):
            break
    parser.write_tree_to_file()
    parser.write_errors_to_file()
    scanner.write_tokens_to_file()
    scanner.write_symbol_table_to_file()
    scanner.write_errors_to_file()


if __name__ == "__main__":
    main()
