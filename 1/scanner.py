"""
Leo Kivikunnas 525925
Jaakko Koskela 526050
"""


import sys


SYMBOL = ["=", ";", ":", ",", "[", "]", "(", ")", "{", "}",
          "+", "-", "*", "=", "<"]
KEYWORD = ["if", "else", "void", "int", "while", "break", "continue", "switch", "default", "case", "return"]

def strip_from_start(string, substring):
    return string.replace(substring, "", 1)


def match_whitespace(string, substring, lineno):
    if substring.isspace():
        if (substring == "\n"):
            lineno += 1

        string = strip_from_start(string, substring)
        return True, string, substring, lineno

    return False, None, None, None


def match_num(string, substring):
    if substring.isdigit():
        for char in string[1:]:
            if char.isdigit():
                substring += char
            else:
                break

        string = strip_from_start(string, substring)
        return True, string, substring

    return False, None, None


def match_symbol(string, substring):
    if substring in SYMBOL:
        if substring == "=" and string[1] == "=":
            substring += string[1]
            string = strip_from_start(string, substring)
        else:
            string = strip_from_start(string, substring)

        return True, string, substring

    return False, None, None


def match_comment(string, substring, lineno):
    if substring == "/":
        if string[1] == "*":
            substring += string[1]
            prev = ""
            for char in string[2:]:
                substring += char
                if char == "\n":
                    lineno += 1
                if prev == "*" and char == "/":
                    break
                prev = char

        if string[1] == "/":
            for char in string[2:]:
                substring += char
                if char == "\n":
                    lineno += 1
                    break

        string = strip_from_start(string, substring)
        return True, string, substring, lineno

    return False, None, None, None


def match_keyword(string, substring):
    if substring in [s[0] for s in KEYWORD]:
        for char in string[1:]:
            substring += char
            if substring in KEYWORD:
                string = strip_from_start(string, substring)
                return True, string, substring
            if len(substring) > len(max(KEYWORD, key=len)):
                break

    return False, None, None


def match_id(string, substring):
    if substring.isalpha():
        for char in string[1:]:
            if char.isdigit() or char.isalpha():
                substring += char
            else:
                string = strip_from_start(string, substring)
                break

        return True, string, substring

    return False, None, None


def match(string, lineno):
    substring = string[0]

    res = match_whitespace(string, substring, lineno)
    matched = res[0]
    new_string = res[1]
    matched_string = res[2]
    new_lineno = res[3]
    if matched:
        token = "whitespace"
        return new_string, token, matched_string, new_lineno

    matched, new_string, matched_string = match_num(string, substring)
    if matched:
        token = "num"
        return new_string, token, matched_string, lineno

    matched, new_string, matched_string = match_symbol(string, substring)
    if matched:
        token = "symbol"
        return new_string, token, matched_string, lineno

    res = match_comment(string, substring, lineno)
    matched = res[0]
    new_string = res[1]
    matched_string = res[2]
    new_lineno = res[3]
    if matched:
        token = "comment"
        return new_string, token, matched_string, new_lineno

    matched, new_string, matched_string = match_keyword(string, substring)
    if matched:
        token = "keyword"
        return new_string, token, matched_string, lineno

    matched, new_string, matched_string = match_id(string, substring)
    if matched:
        token = "id"
        return new_string, token, matched_string, lineno

    sys.exit()

def write_output(token, substring, lineno, out):
    if not lineno in out:
        out[lineno] = []
    out[lineno].append((token, substring))


def report_error(discarded, lineno):
    print(f"line {lineno}: {discarded}, Invalid input")


def handle_match(token, substring, lineno, symbol_table, out):
    if token == "id":
        symbol_table.append(substring)

    write_output(token, substring, lineno, out)


def get_next_token(data, symbol_table, lineno, out):
    data, token, substring, new_lineno = match(data, lineno)
    handle_match(token, substring, lineno, symbol_table, out)
    return data, new_lineno


def main():
    with open("no_errors.txt") as f:
        data = f.read()
        data = data.rstrip("\n")
        f.close

    out = {}
    lineno = 1
    symbol_table = ["if", "else", "void", "int", "while", "break", "continue",
                    "switch", "default", "case", "return"]
    while data:
        data, lineno = get_next_token(data, symbol_table, lineno, out)

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
