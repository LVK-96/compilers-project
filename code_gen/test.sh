#!/bin/sh
tester="samples/Tester"
runtime="./tester_Linux.out"
runtime_output="runtime_output.txt"
sample_runtime_output="sample_runtime_output.txt"

for i in {1..8}
do
    case="T$i"
    input="samples/${case}/input.txt"
    sample_compiler_output="samples/${case}/output.txt"

    echo "${case}:"
    # Run our compiler and pipe the runtime output to a .txt file
    python parser.py $input
    cp output.txt $tester
    cd $tester && $runtime > $runtime_output 2> /dev/null
    cd ../..

    # Run our compiler and pipe the runtime output to a .txt file
    cp $sample_compiler_output $tester
    cd $tester && $runtime > $sample_runtime_output 2> /dev/null
    diff -i -w -s -c $runtime_output $sample_runtime_output
    cd ../..

    echo ""
done
