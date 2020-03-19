#!/bin/sh

for i in {1..6}
do
    case="T$i"
    input="../parser/${case}/input.txt"
    syntax_errors="../parser/${case}/syntax_errors.txt"

    echo "${case}:"
    python parser.py "${input}"
    echo "Syntax errors"
    diff -i -B -Z -s -c "syntax_errors.txt" "${syntax_errors}"
    echo ""
done
