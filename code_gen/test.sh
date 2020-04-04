#!/bin/sh

compiler_output="./output.txt"
tester="./samples/Tester"
runtime_output="${tester}/runtime_out.txt"
sample_runtime_output="${tester}/sample_runtime_out.txt"
runtime="${tester}/tester_Linux.out"
compiled_program_path="${tester}/output.txt"

for i in {1..7}
do
    case="T$i"
    input="./samples/${case}/input.txt"
    sample_compiler_output="./samples/${case}/output.txt"

    echo "${case}:"
    # Compile and run our generated output, copy the runtime output to a .txt file
    python parser.py $input
    cp $compiler_output $compiled_program_path
    $runtime &> $runtime_output

    # Run the sample output and pipe runtime output to a .txt file
    cp $sample_compiler_output $compiled_program_path
    $runtime &> $sample_runtime_output

    # Diff the .txt files
    diff -i -w -s -c $runtime_output $sample_runtime_output
    echo ""
done

# Cleanup
rm $runtime_output $sample_runtime_output $compiled_program_path
