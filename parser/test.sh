#!/bin/sh

for i in {1..6}
do
    case="T${i}"
    tokens="../scanner/${case}/tokens.txt"
    symbol_table="../scanner/${case}/symbol_table.txt"
    lexical_errors="../scanner/${case}/lexical_errors.txt"
    echo "${case}"
    python parser.py "../scanner/${case}/input.txt"
    echo "Tokens: "
    ../are_contents_equal "tokens.txt" "${tokens}"
    echo "Symbol Table: "
    ../are_contents_equal "symbol_table.txt" "${symbol_table}"
    echo "Errors: "
    ../are_contents_equal "lexical_errors.txt" "${lexical_errors}"
    echo ""
done
