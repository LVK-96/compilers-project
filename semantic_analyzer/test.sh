#!/bin/bash

for i in {1..1}
do
    case="T${i}"
    input="${case}/input.txt"
    parse_tree="${case}/parse_tree.txt"
    syntax_errors="${case}/syntax_errors.txt"

    echo "${case}:"
    python parser.py "${input}"
    echo "Tree"
    ../are_contents_equal "parse_tree.txt" "${parse_tree}"
    echo "Syntax errors"
    ../are_contents_equal "syntax_errors.txt" "${syntax_errors}"
    echo ""
done
