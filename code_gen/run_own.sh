compiler_output="./output.txt"
tester="./samples/Tester"
runtime_output="${tester}/runtime_out.txt"
runtime="${tester}/tester_Linux.out"
compiled_program_path="${tester}/output.txt"

python parser.py $1 &&
cp $compiler_output $compiled_program_path &&
$runtime
