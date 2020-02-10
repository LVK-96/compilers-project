#!/bin/sh

python scanner.py T1/input.txt
echo "T1: "
echo "Tokens: "
./are_contents_equal tokens.txt T1/tokens.txt
echo "Symbol Table: "
./are_contents_equal symbol_table.txt T1/symbol_table.txt
echo "Errors: "
./are_contents_equal lexical_errors.txt T1/lexical_errors.txt
echo ""

echo "T2"
python scanner.py T2/input.txt
echo "Tokens: "
./are_contents_equal tokens.txt T2/tokens.txt
echo "Symbol Table: "
./are_contents_equal symbol_table.txt T2/symbol_table.txt
echo "Errors: "
./are_contents_equal lexical_errors.txt T2/lexical_errors.txt
echo ""

echo "T3:"
python scanner.py T3/input.txt
echo "Tokens: "
./are_contents_equal tokens.txt T3/tokens.txt
echo "Symbol Table: "
./are_contents_equal symbol_table.txt T3/symbol_table.txt
echo "Errors: "
./are_contents_equal lexical_errors.txt T3/lexical_errors.txt
echo ""

echo "T4:"
python scanner.py T4/input.txt
echo "Tokens: "
./are_contents_equal tokens.txt T4/tokens.txt
echo "Symbol Table: "
./are_contents_equal symbol_table.txt T4/symbol_table.txt
echo "Errors: "
./are_contents_equal lexical_errors.txt T4/lexical_errors.txt
echo ""

echo "T5:"
python scanner.py T5/input.txt
echo "Tokens: "
./are_contents_equal tokens.txt T5/tokens.txt
echo "Symbol Table: "
./are_contents_equal symbol_table.txt T5/symbol_table.txt
echo "Errors: "
./are_contents_equal lexical_errors.txt T5/lexical_errors.txt
echo ""

echo "T6:"
python scanner.py T6/input.txt
echo "Tokens: "
./are_contents_equal tokens.txt T6/tokens.txt
echo "Symbol Table: "
./are_contents_equal symbol_table.txt T6/symbol_table.txt
echo "Errors: "
./are_contents_equal lexical_errors.txt T6/lexical_errors.txt
echo ""
