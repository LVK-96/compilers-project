import json
import ast

non_terminals = [
    "Program",
    "Declaration-list",
    "Declaration",
    "Declaration-initial",
    "Declaration-prime",
    "Var-declaration-prime",
    "Fun-declaration-prime",
    "Type-specifier",
    "Params",
    "Param-list-void-abtar",
    "Param-list",
    "Param",
    "Param-prime",
    "Compound-stmt",
    "Statement-list",
    "Statement",
    "Expression-stmt",
    "Selection-stmt",
    "Iteration-stmt",
    "Return-stmt",
    "Return-stmt-prime",
    "Switch-stmt",
    "Case-stmts",
    "Case-stmt",
    "Default-stmt",
    "Expression",
    "B",
    "H",
    "Simple-expression-zegond",
    "Simple-expression-prime",
    "C",
    "Relop",
    "Additive-expression",
    "Additive-expression-prime",
    "Additive-expression-zegond",
    "D",
    "Addop",
    "Term",
    "Term-prime",
    "Term-zegond",
    "G",
    "Factor",
    "Var-call-prime",
    "Var-prime",
    "Factor-prime",
    "Factor-zegond",
    "Args",
    "Arg-list",
    "Arg-list-prime"
]

def newfile(filename):

    return open(filename, 'a')


if __name__ == '__main__':
    with open('table.txt', 'r') as f:
        lines = f.readlines()
        j = 0
        for line in lines:
            line = line.strip()#remove whitespaces
            line = line.rstrip(',')
            jsonline = ast.literal_eval(line)
            #jsonline = json.loads(line)
            i = 1
            count = 1
            print(jsonline)
            nextfile = newfile("table1" + str(count) + ".txt")
            nextfile.write(non_terminals[j])
            nextfile.write('&')

            for element in jsonline:
                #print("looping")
                nextfile.write(str(element))

                if(i % 5 == 0):
                    #print("new file")
                    #next file
                    count += 1
                    #close old file and get new one
                    nextfile.write("\\\\ \n")
                    nextfile.write("\hline \n")
                    nextfile.close()
                    nextfile = newfile("table1" + str(count) + ".txt")
                    nextfile.write(non_terminals[j])
                    nextfile.write('&')
                elif(i == 29):
                    #print("new file")
                    #next file
                    count += 1
                    #close old file and get new one
                    nextfile.write("\\\\ \n")
                    nextfile.write("\hline \n")
                    nextfile.close()
                    nextfile = newfile("table1" + str(count) + ".txt")
                    nextfile.write(non_terminals[j])
                    nextfile.write('&')
                else:
                    nextfile.write('&')
                i = i + 1
            print("line done")
            j += 1
            nextfile.close()


        f.close()


        ##to do empty all files in the script that are written to prior to starting appending