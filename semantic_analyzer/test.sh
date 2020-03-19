#!/bin/sh

for i in {1..5}
do
    case="T$i"
    input="samples/${case}/input.txt"
    semantic_errors="samples/${case}/semantic_errors.txt"

    echo "${case}:"
    python parser.py "${input}"
    echo "Semantic errors"
    diff -i -B -Z -s -c "semantic_errors.txt" "${semantic_errors}"
    echo ""
done
