#!/bin/sh

for i in {1..10}
do
    case="CASE$i"
    input="../parser/${case}/input.txt"
    parse_tree="../parser/${case}/parse_tree_ref.txt"
    syntax_errors="../parser/${case}/syntax_errors_ref.txt"

    echo "${case}:"
    python parser.py "${input}"
    echo "Parse Tree"
    diff -i -w -s -c "parse_tree.txt" "${parse_tree}"
    echo "Syntax errors"
    diff -i -w -s -c "syntax_errors.txt" "${syntax_errors}"
    echo ""
done
