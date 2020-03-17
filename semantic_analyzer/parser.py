"""
leo kivikunnas 525925
jaakko koskela 526050
"""
import sys
from collections import OrderedDict
import parser_generator
from scanner import Scanner, SymbolType
from semantic_analyzer import SemanticAnalyzer
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

ll1_table = parser_generator.gen_table()


class LL1_parser:
    def __init__(self, table, terminals, non_terminals, data, filename):
        self.table = table
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.stack = ["$", "Program"]
        self.tree = Node("Program")
        self.current_node = self.tree
        self.errors = []
        self.lineno = 1
        self.latest_type = None
        symbol_table = []
        for keyword in keywords:
            entry = {"name": keyword, "type": SymbolType.KEYWORD}
            symbol_table.append(entry)
        scanner = Scanner(filename, symbols, symbol_table, keywords, data)
        semantic_analyzer = SemanticAnalyzer(symbol_table)
        self.scanner = scanner
        self.semantic_analyzer = semantic_analyzer
        self.input_ptr = self.scanner.get_next_token()

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

        if head.startswith("#"):
            self.semantic_analyzer.semantic_actions(
                head, self.input_ptr, self.latest_type, self.lineno)
            self.stack.pop()

        elif self.input_ptr[to_compare] == head:
            if self.input_ptr[to_compare] == "void" or self.input_ptr[to_compare] == "int":
                self.latest_type = self.input_ptr[to_compare]
            else:
                self.latest_type = "" #reset the latest type
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
            if not item.startswith("#"):
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
    #  placeholder for getting the current input token for semantic analysis
    return ("ID", 1)


def main(argv):
    filename = "input.txt"
    if len(argv) > 0:
        filename = argv[0]
    with open(filename) as f:
        data = f.read()
        data = data.rstrip("\n")
        f.close()

    parser = LL1_parser(
        ll1_table,
        terminals,
        non_terminals,
        data,
        filename
    )
    while True:
        parser.step()
        if (len(parser.stack) < 1):
            break
    parser.write_tree_to_file()
    parser.write_errors_to_file()
    parser.scanner.write_tokens_to_file()
    parser.scanner.write_symbol_table_to_file()
    parser.scanner.write_errors_to_file()
    parser.semantic_analyzer.write_errors_to_file()


if __name__ == "__main__":
    main(sys.argv[1::])
