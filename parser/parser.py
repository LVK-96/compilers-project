import sys
from collections import deque
from scanner import Scanner

symbols = ["=", ";", ":", ",", "[", "]", "(", ")", "{", "}",
               "+", "-", "*", "=", "<"]
keywords = ["if", "else", "void", "int", "while", "break",
                "continue", "switch", "default", "case", "return"]
terminals = ["ID", ";", "[", "NUM", "]", "(", ")", "int", "void", ",", "{", "}",
             "continue", "break", "if", "else", "while", "return", "switch",
             "case", ":", "default", "=", "<", "==", "+", "-", "*", "$"]

production_rules = [
    ("Program", "Declaration-list"),
    ("Declaration-list", "Declaration Declaration-list"),
    ("Declaration-list", "EPSILON"),
    ("Declaration", "Declaration-initial Declaration-prime"),
    ("Declaration-initial", "Type-specifier ID"),
    ("Declaration-prime", "Fun-declaration-prime"),
    ("Declaration-prime", "Var-declaration-prime"),
    ("Var-declaration-prime", ";"),
    ("Var-declaration-prime", "[ NUM ] ;"),
    ("Fun-declaration-prime", "( Params ) Compound-stmt"),
    ("Type-specifier", "int"),
    ("Type-specifier", "void"),
    ("Params", "int ID Param-prime Param-list"),
    ("Params", "void Param-list-void-abtar"),
    ("Param-list-void-abtar", "ID Param-prime Param-list"),
    ("Param-list-void-abtar", "EPSILON"),
    ("Param-list", ", Param Param-list"),
    ("Param-list", "EPSILON"),
    ("Param", "Declaration-initial Param-prime"),
    ("Param-prime", "[ ]"),
    ("Param-prime", "EPSILON"),
    ("Compound-stmt", "{ Declaration-list Statement-list }"),
    ("Statement-list", "Statement Statement-list"),
    ("Statement-list", "EPSILON"),
    ("Statement", "Expression-stmt"),
    ("Statement", "Compound-stmt"),
    ("Statement", "Selection-stmt"),
    ("Statement", "Iteration-stmt"),
    ("Statement", "Return-stmt"),
    ("Statement", "Switch-stmt"),
    ("Expression-stmt", "Expression ;"),
    ("Expression-stmt", "continue ;"),
    ("Expression-stmt", "break ;"),
    ("Expression-stmt", ";"),
    ("Selection-stmt", "if ( Expression ) Statement else Statement"),
    ("Iteration-stmt", "while ( Expression ) Statement"),
    ("Return-stmt", "return Return-stmt-prime"),
    ("Return-stmt-prime", ";"),
    ("Return-stmt-prime", "Expression ;"),
    ("Switch-stmt", "switch ( Expression ) { Case-stmts Default-stmt }"),
    ("Case-stmts", "Case-stmt Case-stmts"),
    ("Case-stmts", "EPSILON"),
    ("Case-stmt", "case NUM : Statement-list"),
    ("Default-stmt", "default : Statement-list"),
    ("Default-stmt", "EPSILON"),
    ("Expression", "Simple-expression-zegond"),
    ("Expression", "ID B"),
    ("B", "= Expression"),
    ("B", "[ Expression ] H"),
    ("B", "Simple-expression-prime"),
    ("H", "= Expression"),
    ("H", "G D C"),
    ("Simple-expression-zegond", "Additive-expression-zegond C"),
    ("Simple-expression-prime", "Additive-expression-prime C"),
    ("C", "Relop Additive-expression"),
    ("C", "EPSILON"),
    ("Relop", "<"),
    ("Relop", "=="),
    ("Additive-expression", "Term D"),
    ("Additive-expression-prime", "Term-prime D"),
    ("Additive-expression-zegond", "Term-zegond D"),
    ("D", "Addop Term D"),
    ("D", "EPSILON"),
    ("Addop", "+"),
    ("Addop", "-"),
    ("Term", "Factor G"),
    ("Term-prime", "Factor-prime G"),
    ("Term-zegond", "Factor-zegond G"),
    ("G", "* Factor G"),
    ("G", "EPSILON"),
    ("Factor", "( Expression )"),
    ("Factor", "ID Var-call-prime"),
    ("Factor", "NUM"),
    ("Var-call-prime", "( Args )"),
    ("Var-call-prime", "Var-prime"),
    ("Var-prime", "[ Expression ]"),
    ("Var-prime", "EPSILON"),
    ("Factor-prime", "( Args )"),
    ("Factor-prime", "EPSILON"),
    ("Factor-zegond", "( Expression )"),
    ("Factor-zegond", "NUM"),
    ("Args", "Arg-list"),
    ("Args", "EPSILON"),
    ("Arg-list", "Expression Arg-list-prime"),
    ("Arg-list-prime", ", Expression Arg-list-prime"),
    ("Arg-list-prime", "EPSILON")
]

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
    "Term"
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
    # ["ID",";","[","NUM","]","(",")","int","void",",","{","}","continue","break","if","else","while","return","switch","case",":","default","=","<","==","+","-","*","$"],
    [88,88,88,88,88,88,88,1,1,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,87],
    [3,3,88,3,88,3,88,2,2,88,3,88,3,3,3,88,3,3,3,88,88,88,88,88,88,88,88,88,3],
    [87,87,88,87,88,87,88,4,4,88,87,88,87,87,87,88,87,87,87,88,88,88,88,88,88,88,88,88,87],
    [88,87,87,88,88,87,87,5,5,87,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88],
    [87,7,7,87,88,6,88,87,87,88,87,88,87,87,87,88,87,87,87,88,88,88,88,88,88,88,88,88,87],
    [87,8,9,87,88,87,88,87,87,88,87,88,87,87,87,88,87,87,87,88,88,88,88,88,88,88,88,88,87],
    [87,87,88,87,88,10,88,87,87,88,87,88,87,87,87,88,87,87,87,88,88,88,88,88,88,88,88,88,87],
    [87,88,88,88,88,88,88,11,12,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88],
    [88,88,88,88,88,88,87,13,14,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88],
    [15,88,88,88,88,88,16,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88],
    [88,88,88,88,88,88,18,88,88,17,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88],
    [88,88,88,88,88,88,87,19,19,87,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88],
    [88,88,20,88,88,88,21,88,88,21,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88],
    [87,87,88,87,88,87,88,87,87,88,22,87,87,87,87,87,87,87,87,87,88,87,88,88,88,88,88,88,87],
    [24,23,88,24,88,24,88,88,88,88,23,24,23,23,23,88,23,23,23,24,88,24,88,88,88,88,88,88,88],
    [25,25,88,25,88,25,88,88,88,88,26,87,25,25,27,87,28,29,30,87,88,87,88,88,88,88,88,88,88],
    [31,34,88,31,88,31,88,88,88,88,87,87,32,33,87,87,87,87,87,87,88,87,88,88,88,88,88,88,88],
    [87,87,88,87,88,87,88,88,88,88,87,87,87,87,35,87,87,87,87,87,88,87,88,88,88,88,88,88,88],
    [87,87,88,87,88,87,88,88,88,88,87,87,87,87,87,87,36,87,87,87,88,87,88,88,88,88,88,88,88],
    [87,87,88,87,88,87,88,88,88,88,87,87,87,87,87,87,87,37,87,87,88,87,88,88,88,88,88,88,88],
    [39,38,88,39,88,39,88,88,88,88,87,87,87,87,87,87,87,87,87,87,88,87,88,88,88,88,88,88,88],
    [87,87,88,87,88,87,88,88,88,88,87,87,87,87,87,87,87,87,40,87,88,87,88,88,88,88,88,88,88],
    [42,88,88,42,88,42,88,88,88,88,88,88,88,88,88,88,88,88,88,41,88,42,88,88,88,88,88,88,88],
    [87,88,88,87,88,87,88,88,88,88,88,88,88,88,88,88,88,88,88,43,88,87,88,88,88,88,88,88,88],
    [88,88,88,88,88,88,88,88,88,88,88,45,88,88,88,88,88,88,88,88,88,44,88,88,88,88,88,88,88],
    [47,87,88,46,87,46,87,88,88,87,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88],
    [88,87,49,88,87,50,87,88,88,87,88,88,88,88,88,88,88,88,88,88,88,88,48,50,50,50,50,50,88],
    [88,87,88,88,87,88,87,88,88,87,88,88,88,88,88,88,88,88,88,88,88,88,51,52,52,52,52,52,88],
    [88,87,88,53,87,53,87,88,88,87,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88],
    [88,87,88,88,87,54,87,88,88,87,88,88,88,88,88,88,88,88,88,88,88,88,88,54,54,54,54,54,88],
    [88,56,88,88,56,88,56,88,88,56,88,88,88,88,88,88,88,88,88,88,88,88,88,55,55,88,88,88,88],
    [87,88,88,87,88,87,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,57,58,88,88,88,88],
    [59,87,88,59,87,59,87,88,88,87,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88],
    [88,87,88,88,87,60,87,88,88,87,88,88,88,88,88,88,88,88,88,88,88,88,88,87,87,60,60,60,88],
    [88,87,88,61,87,61,87,88,88,87,88,88,88,88,88,88,88,88,88,88,88,88,88,87,87,88,88,88,88],
    [88,63,88,88,63,88,63,88,88,63,88,88,88,88,88,88,88,88,88,88,88,88,88,63,63,62,62,88,88],
    [87,88,88,87,88,87,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,64,65,88,88],
    [66,87,88,66,87,66,87,88,88,87,88,88,88,88,88,88,88,88,88,88,88,88,88,87,87,87,87,88,88],
    [88,87,88,88,87,67,87,88,88,87,88,88,88,88,88,88,88,88,88,88,88,88,88,87,87,87,87,67,88],
    [88,87,88,68,87,68,87,88,88,87,88,88,88,88,88,88,88,88,88,88,88,88,88,87,87,87,87,88,88],
    [88,70,88,88,70,88,70,88,88,70,88,88,88,88,88,88,88,88,88,88,88,88,88,70,70,70,70,69,88],
    [72,87,88,73,87,71,87,88,88,87,88,88,88,88,88,88,88,88,88,88,88,88,88,87,87,87,87,87,88],
    [88,87,75,88,87,74,87,88,88,87,88,88,88,88,88,88,88,88,88,88,88,88,88,87,87,87,87,87,88],
    [88,77,76,88,77,88,77,88,88,77,88,88,88,88,88,88,88,88,88,88,88,88,88,77,77,77,77,77,88],
    [88,79,88,88,79,78,79,88,88,79,88,88,88,88,88,88,88,88,88,88,88,88,88,79,79,79,79,79,88],
    [88,87,88,81,87,80,87,88,88,87,88,88,88,88,88,88,88,88,88,88,88,88,88,87,87,87,87,87,88],
    [82,88,88,82,88,82,83,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88],
    [84,88,88,84,88,84,87,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88],
    [88,88,88,88,88,88,86,88,88,85,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88,88]
]

class LL1_parser:
    def __init__(self, table, productions, terminals, non_terminals, data, scanner):
        self.table = table
        self.productions = productions
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.stack = deque(["$", "Program"])
        self.scanner = scanner
        self.data = data
        self.input_ptr = self.scanner.get_next_token()

    def step(self):
        head = self.stack[-1]
        to_compare = 1
        if self.input_ptr[0] == "NUM" or self.input_ptr[0] == "ID":
            to_compare = 0

        print("input ptr", self.input_ptr)
        print("stack", self.stack)
        if self.input_ptr[to_compare] == head:
            popped = self.stack.pop()
            self.input_ptr = self.scanner.get_next_token()
            print(f"pop {head}")

        else:
            column = self.terminals.index(self.input_ptr[to_compare])
            row = self.non_terminals.index(head)
            i = self.table[row][column] - 1
            if i < len(self.productions):
                self.stack.pop()
                production = self.productions[i]
                print("production", production)
                items = production[1].split(" ")
                for item in items[::-1]:
                    if (item != "EPSILON"):
                        self.stack.append(item)
            else:
                # Error
                pass

        print()


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
        production_rules,
        terminals,
        non_terminals,
        data,
        scanner
    )
    while True:
        parser.step()
        if (len(parser.stack) < 1):
            break

    scanner.write_tokens_to_file()
    scanner.write_symbol_table_to_file()
    scanner.write_errors_to_file()


if __name__ == "__main__":
    argv = sys.argv[1:]
    main(argv)
