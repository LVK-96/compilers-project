import sys
from collections import deque
from scanner import Scanner
from anytree import Node, RenderTree

symbols = ["=", ";", ":", ",", "[", "]", "(", ")", "{", "}",
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

ll1_table = [
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'Declaration-list', 'Declaration-list', None, None, None, None, None, None, None, 'Declaration-list'],
    ['EPSILON', 'EPSILON', None, 'EPSILON', None, None, None, None, 'EPSILON', None, 'EPSILON', 'EPSILON', None, None, None, None, None, None, 'EPSILON', None, 'Declaration Declaration-list', 'Declaration Declaration-list', 'EPSILON', 'EPSILON', 'EPSILON', 'EPSILON', 'EPSILON', 'EPSILON', 'EPSILON', 'EPSILON'],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'Declaration-initial Declaration-prime', 'Declaration-initial Declaration-prime', None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'Type-specifier ID', 'Type-specifier ID', None, None, None, None, None, None, None, None],
    [None, None, None, 'Var-declaration-prime', None, None, 'Var-declaration-prime', None, 'Fun-declaration-prime', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, ';', None, None, '[ NUM ] ;', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, '( Params ) Compound-stmt', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'void', 'int', None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'void Param-list-void-abtar', 'int ID Param-prime Param-list', None, None, None, None, None, None, None, None],
    ['ID Param-prime Param-list', None, None, None, None, None, None, None, None, 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, ', Param Param-list', None, None, None, 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'Declaration-initial Param-prime', 'Declaration-initial Param-prime', None, None, None, None, None, None, None, None],
    [None, None, None, None, None, 'EPSILON', '[ ]', None, None, 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, '{ Declaration-list Statement-list }', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    ['Statement Statement-list', 'Statement Statement-list', None, 'Statement Statement-list', None, None, None, None, 'Statement Statement-list', None, 'Statement Statement-list', 'EPSILON', None, None, None, None, None, None, 'Statement Statement-list', None, None, None, 'Statement Statement-list', 'Statement Statement-list', 'Statement Statement-list', 'Statement Statement-list', 'EPSILON', 'EPSILON', 'Statement Statement-list', None],
    ['Expression-stmt', 'Expression-stmt', None, 'Expression-stmt', None, None, None, None, 'Expression-stmt', None, 'Compound-stmt', None, None, None, None, None, None, None, 'Selection-stmt', None, None, None, 'Iteration-stmt', 'Expression-stmt', 'Expression-stmt', 'Switch-stmt', None, None, 'Return-stmt', None],
    ['Expression ;', 'Expression ;', None, ';', None, None, None, None, 'Expression ;', None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'break ;', 'continue ;', None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'if ( Expression ) Statement else Statement', None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'while ( Expression ) Statement', None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'return Return-stmt-prime', None],
    ['Expression ;', 'Expression ;', None, ';', None, None, None, None, 'Expression ;', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'switch ( Expression ) { Case-stmts Default-stmt }', None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'EPSILON', 'Case-stmt Case-stmts', None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'case NUM : Statement-list', None, None],
    [None, None, None, None, None, None, None, None, None, None, None, 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'default : Statement-list', None, None, None],
    ['ID B', 'Simple-expression-zegond', None, None, None, None, None, None, 'Simple-expression-zegond', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, '= Expression', 'Simple-expression-prime', None, 'Simple-expression-prime', '[ Expression ] H', 'Simple-expression-prime', 'Simple-expression-prime', 'Simple-expression-prime', None, None, 'Simple-expression-prime', 'Simple-expression-prime', 'Simple-expression-prime', None, 'Simple-expression-prime', 'Simple-expression-prime', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, '= Expression', 'G D C', None, 'G D C', None, 'G D C', None, 'G D C', None, None, 'G D C', 'G D C', 'G D C', None, 'G D C', 'G D C', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, 'Additive-expression-zegond C', None, None, None, None, None, None, 'Additive-expression-zegond C', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, 'Additive-expression-prime C', None, 'Additive-expression-prime C', None, 'Additive-expression-prime C', 'Additive-expression-prime C', 'Additive-expression-prime C', None, None, 'Additive-expression-prime C', 'Additive-expression-prime C', 'Additive-expression-prime C', None, 'Additive-expression-prime C', 'Additive-expression-prime C', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, 'EPSILON', None, 'EPSILON', None, 'EPSILON', None, 'EPSILON', None, None, None, None, None, None, 'Relop Additive-expression', 'Relop Additive-expression', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, '<', '==', None, None, None, None, None, None, None, None, None, None, None, None],
    ['Term D', 'Term D', None, None, None, None, None, None, 'Term D', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, 'Term-prime D', None, 'Term-prime D', None, 'Term-prime D', 'Term-prime D', 'Term-prime D', None, None, 'Term-prime D', 'Term-prime D', 'Term-prime D', None, 'Term-prime D', 'Term-prime D', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, 'Term-zegond D', None, None, None, None, None, None, 'Term-zegond D', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, 'EPSILON', None, 'EPSILON', None, 'EPSILON', None, 'EPSILON', None, None, 'Addop Term D', 'Addop Term D', None, None, 'EPSILON', 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, None, None, None, None, '+', '-', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    ['Factor G', 'Factor G', None, None, None, None, None, None, 'Factor G', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, 'Factor-prime G', None, 'Factor-prime G', None, 'Factor-prime G', 'Factor-prime G', 'Factor-prime G', None, None, 'Factor-prime G', 'Factor-prime G', 'Factor-prime G', None, 'Factor-prime G', 'Factor-prime G', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, 'Factor-zegond G', None, None, None, None, None, None, 'Factor-zegond G', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, 'EPSILON', None, 'EPSILON', None, 'EPSILON', None, 'EPSILON', None, None, 'EPSILON', 'EPSILON', '* Factor G', None, 'EPSILON', 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None],
    ['ID Var-call-prime', 'NUM', None, None, None, None, None, None, '( Expression )', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, 'Var-prime', None, 'Var-prime', 'Var-prime', 'Var-prime', '( Args )', 'Var-prime', None, None, 'Var-prime', 'Var-prime', 'Var-prime', None, 'Var-prime', 'Var-prime', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, 'EPSILON', None, 'EPSILON', '[ Expression ]', 'EPSILON', None, 'EPSILON', None, None, 'EPSILON', 'EPSILON', 'EPSILON', None, 'EPSILON', 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, 'EPSILON', None, 'EPSILON', None, 'EPSILON', '( Args )', 'EPSILON', None, None, 'EPSILON', 'EPSILON', 'EPSILON', None, 'EPSILON', 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, 'NUM', None, None, None, None, None, None, '( Expression )', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    ['Arg-list', 'Arg-list', None, None, None, None, None, None, 'Arg-list', 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    ['Expression Arg-list-prime', 'Expression Arg-list-prime', None, None, None, None, None, None, 'Expression Arg-list-prime', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, None, ', Expression Arg-list-prime', None, None, None, 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
]

class LL1_parser:
    def __init__(self, table, terminals, non_terminals, data, scanner):
        self.table = table
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.stack = deque(["$", "Program"])
        self.scanner = scanner
        self.data = data
        self.input_ptr = self.scanner.get_next_token()
        self.tree = Node("Program")
        self.current_node = self.tree

    def step(self):
        head = self.stack[-1]
        to_compare = 1
        if self.input_ptr[0] == "NUM" or self.input_ptr[0] == "ID":
            to_compare = 0

        print("input ptr", self.input_ptr)
        print("stack", self.stack)
        if self.input_ptr[to_compare] == head:
            popped = self.stack.pop()
            if(popped != '$'):
                self.add_nodes(popped, [], self.input_ptr)
            self.input_ptr = self.scanner.get_next_token()
            print(f"pop {head}")

        else:
            column = self.terminals.index(self.input_ptr[to_compare])
            row = self.non_terminals.index(head) if head in self.non_terminals else None
            production = ll1_table[row][column] if row != None else None
            if production:
                self.stack.pop()
                print("production", production)
                items = production.split(" ")
                #add nodes to tree
                self.add_nodes(start, items, self.input_ptr)
                for item in items[::-1]:
                    if (item != "EPSILON"):
                        self.stack.append(item)
            else:
                # Error
                sys.exit(1)

        print()
    
    #start is the lhs o production and items make up the rhs
    def add_nodes(self, start, items, input_ptr):
        print("start: ", start)
        #find the start point
        while(self.current_node.name != start):
            #move up
            self.current_node = self.current_node.parent
            #check children for start
            for child in self.current_node.children:
                if child.name == start:
                    #start found move there
                    self.current_node = child
                    break
            #when to break

        left_node = None

        #add in reverse order and continue to last 
        for item in items[::-1]:
            if (item != "EPSILON"):
                #add nodes
                left_node = Node(item, parent=self.current_node)


        #add terminals from input - there should be no items in items - could be added before calling this function 
        if(self.current_node.name == "ID" or self.current_node.name == "NUM"):
            #add variable ID or NUM to tree from input
            print("adding a variable")
            Node(input_ptr[1], parent=self.current_node)

        #move to leftmost node - probably not needed anymore
        if(left_node):
            self.current_node = left_node




    def write_tree_to_file(self):
        for pre, _, node in RenderTree(self.tree):
            print("%s%s" % (pre, node.name))



def main(argv):
    filename = "input.txt"
    # TODO: Remove this before turn in
    if argv and argv[0]:
        filename = argv[0]

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
    scanner.write_tokens_to_file()
    scanner.write_symbol_table_to_file()
    scanner.write_errors_to_file()


if __name__ == "__main__":
    argv = sys.argv[1:]
    main(argv)
