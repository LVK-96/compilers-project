"""
Leo Kivikunnas 525925
Jaakko Koskela 526050
"""

import re


KEYWORD = r"if|else|void|int|while|break|continue|switch|default|case|return"
ID = r"[A-Za-z][A-Za-z0-9]*"
NUM = r"[0-9]+"
SYMBOL = r"==|[;:,\[\]\(\)\{\}\+\-\*\=\<]"
COMMENT = r"\/\*.*\*\/|//.*\n"
WHITESPACE = r"[\ \n\r\t\v\f]"


def match(string):
    m = re.match(KEYWORD, string)
    if m:
        return "keyword", m.group(0)

    m = re.match(ID, string)
    if m:
        return "id", m.group(0)

    m = re.match(NUM, string)
    if m:
        return "num", m.group(0)

    m = re.match(SYMBOL, string)
    if m:
        return "symbol", m.group(0)

    m = re.match(COMMENT, string)
    if m:
        return "comment", m.group(0)

    m = re.match(WHITESPACE, string)
    if m:
        return "whitespace", m.group(0)

    else:
        return None


def write_output(token, sub_string, lineno, out):
    if not lineno in out:
        out[lineno] = []
    out[lineno].append((token, sub_string))


def report_error(discarded, lineno):
    print(f"line {lineno}: {discarded}, Invalid input")


def handle_match(matched, lineno, symbol_table, out):
    token = matched[0]
    sub_string = matched[1]
    if token == "id":
        symbol_table.append(sub_string)

    write_output(token, sub_string, lineno, out)


def main():
    with open("test_input.txt") as f:
        data = f.read()
        data = data.rstrip("\n")
        f.close

    out = {}
    lineno = 1
    symbol_table = ["if", "else", "void", "int", "while", "break", "continue",
                    "switch", "default", "case", "return"]
    while data:
        matched = match(data)
        if matched:
            handle_match(matched, lineno, symbol_table, out)
            lineno += matched[1].count("\n")
            data = data.replace(matched[1], "", 1)

        else:
            # Remove previous token if it is not whitespace or comment
            discarded = ""
            if lineno in out:
                prev = out[lineno][-1]
                if prev[0] not in ["whitespace", "comment"]:
                    if prev[0] == "id":
                        symbol_table.pop()
                    tmp = out[lineno].pop()
                    discarded += tmp[1]

            # Delete input untill next valid token is found
            while not matched:
                discarded += data[:1]
                data = data[1:]
                matched = match(data)

            handle_match(matched, lineno, symbol_table, out)
            lineno += matched[1].count("\n")
            report_error(discarded, lineno)
            data = data.replace(matched[1], "", 1)

    print("\nTokens:")
    for key in out:
        out[key] = [t for t in out[key] if t[0] not in ["whitespace", "comment"]]
        if len(out[key]) > 0:
            print(out[key])


    symbol_table = list(dict.fromkeys(symbol_table))
    print("\nSymbol table:")
    print(symbol_table)


if __name__ == "__main__":
    main()
