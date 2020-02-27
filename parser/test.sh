#!/bin/sh

for i in {1..6}
do
    case="T${i}"
    input="${case}/input.txt"
    parse_tree="${case}/parse_tree.txt"
    syntax_errors="${case}/syntax_errors.txt"

    echo "${case}:"
    python parser.py "${input}"
    ../are_contents_equal "parse_tree.txt" "${parse_tree}"
    echo ""
done
