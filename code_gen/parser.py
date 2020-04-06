"""
leo kivikunnas 525925
jaakko koskela 526050
"""

from anytree import Node, RenderTree
from scanner import Scanner, SymbolType
from semantic_analyzer import SemanticAnalyzer
from code_gen import CodeGenerator

symbols = [";", ":", ",", "[", "]", "(", ")", "{", "}", "+", "-", "*", "=", "<", "=="]
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

ll1_table_no_action_symbols = [
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
    [None, None, None, None, ', Expression Arg-list-prime', None, None, None, 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
]

ll1_table = [
    [None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, '#START Declaration-list #END', '#START Declaration-list #END', None, None, None, None, None, None, None, '#START Declaration-list #END'],
    ['EPSILON', 'EPSILON', 'EPSILON', None, None, None, None, 'EPSILON', None, 'EPSILON', 'EPSILON', None, None, None, None, None, None, 'EPSILON', None, 'Declaration Declaration-list', 'Declaration Declaration-list', 'EPSILON', 'EPSILON', 'EPSILON', 'EPSILON', 'EPSILON', 'EPSILON', 'EPSILON', 'EPSILON'],
    ['SYNCH', 'SYNCH', 'SYNCH', None, None, None, None, 'SYNCH', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, 'SYNCH', None, 'Declaration-initial Declaration-prime', 'Declaration-initial Declaration-prime', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH'],
    [None, None, 'SYNCH', None, 'SYNCH', 'SYNCH', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, None, None, None, None, 'Type-specifier #PID ID', 'Type-specifier #PID ID', None, None, None, None, None, None, None, None],
    ['SYNCH', 'SYNCH', '#VARIABLE Var-declaration-prime', None, None, '#VARIABLE Var-declaration-prime', None, '#FUNCTION Fun-declaration-prime', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, 'SYNCH', None, 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH'],
    ['SYNCH', 'SYNCH', ';', None, None, '#ARRAY [ #ARRAY_SIZE NUM ] ;', None, 'SYNCH', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, 'SYNCH', None, 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH'],
    ['SYNCH', 'SYNCH', 'SYNCH', None, None, None, None, '#BEGINSCOPE ( #START_PARAM_COUNTER Params #STOP_PARAM_COUNTER ) Compound-stmt #ENDSCOPE', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, 'SYNCH', None, 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH'],
    ['SYNCH', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'void', 'int', None, None, None, None, None, None, None, None],
    [None, None, None, None, None, None, None, None, 'SYNCH', None, None, None, None, None, None, None, None, None, None, 'void Param-list-void-abtar', 'int #PID ID Param-prime Param-list', None, None, None, None, None, None, None, None],
    ['#PID ID Param-prime Param-list', None, None, None, None, None, None, None, 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, ', Param Param-list', None, None, None, 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, 'SYNCH', None, None, None, 'SYNCH', None, None, None, None, None, None, None, None, None, None, 'Declaration-initial Param-prime', 'Declaration-initial Param-prime', None, None, None, None, None, None, None, None],
    [None, None, None, None, '#PARAM EPSILON', '#ARRAY #ARRAY_PARAM [ ]', None, None, '#PARAM EPSILON', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    ['SYNCH', 'SYNCH', 'SYNCH', None, None, None, None, 'SYNCH', None, '{ Declaration-list #STATEMENTS_BEGIN Statement-list }', 'SYNCH', None, None, None, None, None, None, 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH'],
    ['Statement Statement-list', 'Statement Statement-list', 'Statement Statement-list', None, None, None, None, 'Statement Statement-list', None, 'Statement Statement-list', 'EPSILON', None, None, None, None, None, None, 'Statement Statement-list', None, None, None, 'Statement Statement-list', 'Statement Statement-list', 'Statement Statement-list', 'Statement Statement-list', 'EPSILON', 'EPSILON', 'Statement Statement-list', None],
    ['Expression-stmt', 'Expression-stmt', 'Expression-stmt', None, None, None, None, 'Expression-stmt', None, 'Compound-stmt', 'SYNCH', None, None, None, None, None, None, 'Selection-stmt', 'SYNCH', None, None, 'Iteration-stmt', 'Expression-stmt', 'Expression-stmt', 'Switch-stmt', 'SYNCH', 'SYNCH', 'Return-stmt', None],
    ['#START_TYPE_CHECK Expression #TYPE_CHECK ;', '#START_TYPE_CHECK Expression #TYPE_CHECK ;', '#TYPE_CHECK ;', None, None, None, None, '#START_TYPE_CHECK Expression #TYPE_CHECK ;', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, 'SYNCH', 'SYNCH', None, None, 'SYNCH', '#BREAK break ;', '#CONTINUE continue ;', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', None],
    ['SYNCH', 'SYNCH', 'SYNCH', None, None, None, None, 'SYNCH', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, 'if ( #START_TYPE_CHECK Expression #TYPE_CHECK_IN_BRACKETS ) #SAVE Statement else #JPF_SAVE Statement #JP', 'SYNCH', None, None, 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', None],
    ['SYNCH', 'SYNCH', 'SYNCH', None, None, None, None, 'SYNCH', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, 'SYNCH', 'SYNCH', None, None, 'while #ENTER_WHILE ( #START_TYPE_CHECK Expression #TYPE_CHECK_IN_BRACKETS ) #SAVE Statement #EXIT_WHILE', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', None],
    ['SYNCH', 'SYNCH', 'SYNCH', None, None, None, None, 'SYNCH', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, 'SYNCH', 'SYNCH', None, None, 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'return Return-stmt-prime #RETURN', None],
    ['#START_TYPE_CHECK Expression #TYPE_CHECK ;', '#START_TYPE_CHECK Expression #TYPE_CHECK ;', '; #EMPTY_RETURN', None, None, None, None, '#START_TYPE_CHECK Expression #TYPE_CHECK ;', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, 'SYNCH', 'SYNCH', None, None, 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', 'SYNCH', None],
    ['SYNCH', 'SYNCH', 'SYNCH', None, None, None, None, 'SYNCH', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, 'SYNCH', 'SYNCH', None, None, 'SYNCH', 'SYNCH', 'SYNCH', 'switch #ENTER_SWITCH_CASE ( #START_TYPE_CHECK Expression #TYPE_CHECK_IN_BRACKETS ) { Case-stmts Default-stmt } #EXIT_SWITCH_CASE', 'SYNCH', 'SYNCH', 'SYNCH', None],
    [None, None, None, None, None, None, None, None, None, None, 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'EPSILON', 'Case-stmt Case-stmts', None, None],
    [None, None, None, None, None, None, None, None, None, None, 'SYNCH', None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'SYNCH', 'case #IMMEDIATE NUM #SAVE_CASE : Statement-list', None, None],
    [None, None, None, None, None, None, None, None, None, None, 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None, None, None, 'default : #DEFAULT_CASE Statement-list', None, None, None],
    ['#USE_PID #ADD_TO_TYPE_CHECK ID B', 'Simple-expression-zegond', 'SYNCH', None, 'SYNCH', None, 'SYNCH', 'Simple-expression-zegond', 'SYNCH', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, 'Simple-expression-prime', None, 'Simple-expression-prime', '#NOT_FUNCTION_CALL [ #INDEXING #START_TYPE_CHECK Expression #TYPE_CHECK #INDEXING_DONE ] H', 'Simple-expression-prime', 'Simple-expression-prime', 'Simple-expression-prime', None, None, 'Simple-expression-prime', 'Simple-expression-prime', 'Simple-expression-prime', '#NOT_FUNCTION_CALL #ASSIGNMENT_CHAIN = Expression #ASSIGN', 'Simple-expression-prime', 'Simple-expression-prime', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, 'G D C', None, 'G D C', None, 'G D C', None, 'G D C', None, None, 'G D C', 'G D C', 'G D C', '#ASSIGNMENT_CHAIN = Expression #ASSIGN', 'G D C', 'G D C', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, 'Additive-expression-zegond C', 'SYNCH', None, 'SYNCH', None, 'SYNCH', 'Additive-expression-zegond C', 'SYNCH', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, 'Additive-expression-prime C', None, 'Additive-expression-prime C', None, 'Additive-expression-prime C', 'Additive-expression-prime C', 'Additive-expression-prime C', None, None, 'Additive-expression-prime C', 'Additive-expression-prime C', 'Additive-expression-prime C', None, 'Additive-expression-prime C', 'Additive-expression-prime C', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, 'EPSILON', None, 'EPSILON', None, 'EPSILON', None, 'EPSILON', None, None, None, None, None, None, 'Relop Additive-expression #RELOP', 'Relop Additive-expression #RELOP', None, None, None, None, None, None, None, None, None, None, None, None],
    ['SYNCH', 'SYNCH', None, None, None, None, None, 'SYNCH', None, None, None, None, None, None, None, '< #LT', '== #EQ', None, None, None, None, None, None, None, None, None, None, None, None],
    ['Term D', 'Term D', 'SYNCH', None, 'SYNCH', None, 'SYNCH', 'Term D', 'SYNCH', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, 'Term-prime D', None, 'Term-prime D', None, 'Term-prime D', 'Term-prime D', 'Term-prime D', None, None, 'Term-prime D', 'Term-prime D', 'Term-prime D', None, 'Term-prime D', 'Term-prime D', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, 'Term-zegond D', 'SYNCH', None, 'SYNCH', None, 'SYNCH', 'Term-zegond D', 'SYNCH', None, None, None, None, None, None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, 'EPSILON', None, 'EPSILON', None, 'EPSILON', None, 'EPSILON', None, None, 'Addop Term #ADDOP D', 'Addop Term #ADDOP D', None, None, 'EPSILON', 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None],
    ['SYNCH', 'SYNCH', None, None, None, None, None, 'SYNCH', None, None, None, '#PLUS +', '#MINUS -', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    ['Factor G', 'Factor G', 'SYNCH', None, 'SYNCH', None, 'SYNCH', 'Factor G', 'SYNCH', None, None, 'SYNCH', 'SYNCH', None, None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, 'Factor-prime G', None, 'Factor-prime G', None, 'Factor-prime G', 'Factor-prime G', 'Factor-prime G', None, None, 'Factor-prime G', 'Factor-prime G', 'Factor-prime G', None, 'Factor-prime G', 'Factor-prime G', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, 'Factor-zegond G', 'SYNCH', None, 'SYNCH', None, 'SYNCH', 'Factor-zegond G', 'SYNCH', None, None, 'SYNCH', 'SYNCH', None, None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, 'EPSILON', None, 'EPSILON', None, 'EPSILON', None, 'EPSILON', None, None, 'EPSILON', 'EPSILON', '* Factor #MULT G', None, 'EPSILON', 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None],
    ['#USE_PID #ADD_TO_TYPE_CHECK ID Var-call-prime', '#ADD_TO_TYPE_CHECK #IMMEDIATE NUM', 'SYNCH', None, 'SYNCH', None, 'SYNCH', '( #START_TYPE_CHECK Expression #TYPE_CHECK_IN_BRACKETS )', 'SYNCH', None, None, 'SYNCH', 'SYNCH', 'SYNCH', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, '#NOT_FUNCTION_CALL Var-prime', None, '#NOT_FUNCTION_CALL Var-prime', '#NOT_FUNCTION_CALL Var-prime', '#NOT_FUNCTION_CALL Var-prime', '#FUNCTION_CALL ( #START_ARGUMENT_COUNTER Args #STOP_ARGUMENT_COUNTER ) #FUNCTION_CALLED', '#NOT_FUNCTION_CALL Var-prime', None, None, '#NOT_FUNCTION_CALL Var-prime', '#NOT_FUNCTION_CALL Var-prime', '#NOT_FUNCTION_CALL Var-prime', None, '#NOT_FUNCTION_CALL Var-prime', '#NOT_FUNCTION_CALL Var-prime', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, 'EPSILON', None, 'EPSILON', '[ #INDEXING #START_TYPE_CHECK Expression #TYPE_CHECK #INDEXING_DONE ]', 'EPSILON', None, 'EPSILON', None, None, 'EPSILON', 'EPSILON', 'EPSILON', None, 'EPSILON', 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, '#NOT_FUNCTION_CALL EPSILON', None, '#NOT_FUNCTION_CALL EPSILON', None, '#NOT_FUNCTION_CALL EPSILON', '#FUNCTION_CALL ( #START_ARGUMENT_COUNTER Args #STOP_ARGUMENT_COUNTER ) #FUNCTION_CALLED', '#NOT_FUNCTION_CALL EPSILON', None, None, '#NOT_FUNCTION_CALL EPSILON', '#NOT_FUNCTION_CALL EPSILON', '#NOT_FUNCTION_CALL EPSILON', None, '#NOT_FUNCTION_CALL EPSILON', '#NOT_FUNCTION_CALL EPSILON', None, None, None, None, None, None, None, None, None, None, None, None],
    [None, '#ADD_TO_TYPE_CHECK #IMMEDIATE NUM', 'SYNCH', None, 'SYNCH', None, 'SYNCH', '( #START_TYPE_CHECK Expression #TYPE_CHECK_IN_BRACKETS )', 'SYNCH', None, None, 'SYNCH', 'SYNCH', 'SYNCH', None, 'SYNCH', 'SYNCH', None, None, None, None, None, None, None, None, None, None, None, None],
    ['Arg-list', 'Arg-list', None, None, None, None, None, 'Arg-list', 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    ['#ARGUMENT #START_TYPE_CHECK Expression #ARGUMENT_TO_PASS #TYPE_CHECK Arg-list-prime', '#ARGUMENT #START_TYPE_CHECK Expression #ARGUMENT_TO_PASS #TYPE_CHECK Arg-list-prime', None, None, None, None, None, '#ARGUMENT #START_TYPE_CHECK Expression #ARGUMENT_TO_PASS #TYPE_CHECK Arg-list-prime', 'SYNCH', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None],
    [None, None, None, None, ', #ARGUMENT #START_TYPE_CHECK Expression #ARGUMENT_TO_PASS #TYPE_CHECK Arg-list-prime', None, None, None, 'EPSILON', None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None]
]


class LL1_parser:
    def __init__(self, table, table_no_action_symbols, terminals, non_terminals, data, filename):
        self.table = table
        self.table_no_action_symbols = table_no_action_symbols
        self.terminals = terminals
        self.non_terminals = non_terminals
        self.stack = ["$", "Program"]
        self.tree = Node("Program")
        self.current_node = self.tree
        self.errors = []
        self.syntax_error_occured = False
        self.semantic_error_occured = False
        self.lineno = 1
        self.latest_type = None
        symbol_table = []
        scope_stack = [0]
        for keyword in keywords:
            entry = {"name": keyword, "type": SymbolType.KEYWORD}
            symbol_table.append(entry)
        scanner = Scanner(filename, symbols, symbol_table, keywords, data, scope_stack)
        semantic_analyzer = SemanticAnalyzer(symbol_table, scope_stack)
        code_gen = CodeGenerator(symbol_table, scope_stack)
        self.scanner = scanner
        self.semantic_analyzer = semantic_analyzer
        self.code_gen = code_gen
        self.input_ptr = self.scanner.get_next_token()

    def remove_node(self, name):
        # Used in error handling to remove all nonterminals of a node
        orig_node = self.current_node
        found = False
        while not found:
            if self.current_node.parent:
                self.current_node = self.current_node.parent
                for child in self.current_node.children:
                    if not child.children and child.name == name:
                        child.parent = None
                        found = True
                        break
            else:
                # This means that the current node has no parent
                # -> We cannot continue our search
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
                        row = self.table_no_action_symbols[i]
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
        self.syntax_error_occured = True
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
            self.remove_node(popped)
            if popped in non_terminals:
                # Synch
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
            self.semantic_error_occured = self.semantic_analyzer.semantic_actions(
                head, self.input_ptr, self.latest_type, self.lineno)
            if not self.semantic_error_occured and not self.syntax_error_occured:
                # Only run code gen if there are no errors
                self.code_gen.semantic_actions(head, self.input_ptr)
            self.stack.pop()

        elif self.input_ptr[to_compare] == head:
            if self.input_ptr[to_compare] == "void" or self.input_ptr[to_compare] == "int":
                self.latest_type = (
                    SymbolType.INT if self.input_ptr[to_compare] == "int"
                    else SymbolType.VOID
                )
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
            production = self.table[row][column] if row is not None else None
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
        found = False
        while not found:
            # move up
            if self.current_node.parent:
                self.current_node = self.current_node.parent
                # check children for start
                for child in self.current_node.children:
                    if child.name == start and not child.children:
                        # start found move there
                        self.current_node = child
                        found = True
                        break
            elif self.current_node.name == start and not self.current_node.children:
                found = True

        if found:
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


def main():
    filename = "input.txt"
    with open(filename) as f:
        data = f.read()
        data = data.rstrip("\n")
        f.close()

    parser = LL1_parser(
        ll1_table,
        ll1_table_no_action_symbols,
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
    parser.code_gen.write_output_to_file()


if __name__ == "__main__":
    main()
