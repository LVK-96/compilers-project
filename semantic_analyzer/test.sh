#!/bin/sh

for i in {1..4}
do
    case="T{$i}"
    input="samples/${case}/input.txt"
    semantic_errors="samples/${case}/semantic_errors.txt"

    echo "${case}:"
    python parser.py "${input}"
    echo "Semantic errors"
    ../are_contents_equal "syntax_errors.txt" "${semantic_errors}"
    echo ""
done
