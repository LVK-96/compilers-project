#!/bin/sh

for i in {1..6}
do
    case="T${i}"
    input="../scanner/${case}/input.txt"
    tokens="../scanner/${case}/tokens.txt"
    symbol_table="../scanner/${case}/symbol_table.txt"
    lexical_errors="../scanner/${case}/lexical_errors.txt"

    echo "${case}:"
    python parser.py "${input}"
    echo "Tokens: "
    ../are_contents_equal "tokens.txt" "${tokens}"
    echo "Symbol Table: "
    ../are_contents_equal "symbol_table.txt" "${symbol_table}"
    echo "Errors: "
    ../are_contents_equal "lexical_errors.txt" "${lexical_errors}"
    echo ""
done
