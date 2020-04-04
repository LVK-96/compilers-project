tester="./samples/Tester"
sample_runtime_output="${tester}/sample_runtime_out.txt"
runtime="${tester}/tester_Linux.out"
compiled_program_path="${tester}/output.txt"

cp $1 $compiled_program_path &&
$runtime
