#!/bin/sh

python parser.py ../scanner/T1/input.txt
echo "T1: "
echo "Tokens: "
../are_contents_equal tokens.txt ../scanner/T1/tokens.txt
echo "Symbol Table: "
../are_contents_equal symbol_table.txt ../scanner/T1/symbol_table.txt
echo "Errors: "
../are_contents_equal lexical_errors.txt ../scanner/T1/lexical_errors.txt
echo ""

echo "T2"
python parser.py ../scanner/T2/input.txt
echo "Tokens: "
../are_contents_equal tokens.txt ../scanner/T2/tokens.txt
echo "Symbol Table: "
../are_contents_equal symbol_table.txt ../scanner/T2/symbol_table.txt
echo "Errors: "
../are_contents_equal lexical_errors.txt ../scanner/T2/lexical_errors.txt
echo ""

echo "T3:"
python parser.py ../scanner/T3/input.txt
echo "Tokens: "
../are_contents_equal tokens.txt ../scanner/T3/tokens.txt
echo "Symbol Table: "
../are_contents_equal symbol_table.txt ../scanner/T3/symbol_table.txt
echo "Errors: "
../are_contents_equal lexical_errors.txt ../scanner/T3/lexical_errors.txt
echo ""

echo "T4:"
python parser.py ../scanner/T4/input.txt
echo "Tokens: "
../are_contents_equal tokens.txt ../scanner/T4/tokens.txt
echo "Symbol Table: "
../are_contents_equal symbol_table.txt ../scanner/T4/symbol_table.txt
echo "Errors: "
../are_contents_equal lexical_errors.txt ../scanner/T4/lexical_errors.txt
echo ""

echo "T5:"
python parser.py ../scanner/T5/input.txt
echo "Tokens: "
../are_contents_equal tokens.txt ../scanner/T5/tokens.txt
echo "Symbol Table: "
../are_contents_equal symbol_table.txt ../scanner/T5/symbol_table.txt
echo "Errors: "
../are_contents_equal lexical_errors.txt ../scanner/T5/lexical_errors.txt
echo ""

echo "T6:"
python parser.py ../scanner/T6/input.txt
echo "Tokens: "
../are_contents_equal tokens.txt ../scanner/T6/tokens.txt
echo "Symbol Table: "
../are_contents_equal symbol_table.txt ../scanner/T6/symbol_table.txt
echo "Errors: "
../are_contents_equal lexical_errors.txt ../scanner/T6/lexical_errors.txt
echo ""
