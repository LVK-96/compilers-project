"""
Leo Kivikunnas 525925
Jaakko Koskela 526050
"""


import sys


SYMBOL = ["=", ";", ":", ",", "[", "]", "(", ")", "{", "}",
          "+", "-", "*", "=", "<"]
KEYWORD = ["if", "else", "void", "int", "while", "break", "continue", "switch", "default", "case", "return"]

def starts_valid_token(char, n):
    if char and n:
        return char.isspace() or char.isdigit() or char.isalpha() or char in SYMBOL or (char == "/" and (n == "*" or n == "/"))
    elif char:
        return char.isspace() or char.isalpha() or chra.isnum() or char in SYMBOL
    else:
        return True

def strip_from_start(string, substring):
    return string.replace(substring, "", 1)


def report_error(discarded, lineno):
    print(f"line {lineno}: {discarded}, Invalid input")

def gather_invalid_char(string):
    substring = ""
    for i, char in enumerate(string):
        n = string[i + 1] if i + 1 < len(string) else None
        if starts_valid_token(char, n):
            break

        substring += char

    return substring


def match_whitespace(string, substring, lineno):
    if substring.isspace():
        if (substring == "\n"):
            lineno += 1

        string = strip_from_start(string, substring)
        return True, string, substring, lineno

    return False, None, None, lineno


def match_num(string, substring, lineno):
    if substring.isdigit():
        for char in string[1:]:
            if char.isdigit():
                substring += char
            elif char in SYMBOL or char.isspace():
                break
            else:
                substring += char
                string = strip_from_start(string, substring)
                second_substring = gather_invalid_char(string[1:])
                string = strip_from_start(string, second_substring)
                return False, string, substring + second_substring, lineno

        string = strip_from_start(string, substring)
        return True, string, substring, lineno

    return False, None, None, lineno


def match_symbol(string, substring, lineno):
    if substring in SYMBOL:
        n = string[1] if 1 < len(string) else None
        nn = string[2] if 2 < len(string) else None
        if substring != "=" and substring in SYMBOL and starts_valid_token(n, nn):
            string = strip_from_start(string, substring)
            return True, string, substring, lineno

        if substring == "=" and n == "=":
            substring += n
            string = strip_from_start(string, substring)
            return True, string, substring, lineno

        if (substring == "=" and n != "=" and starts_valid_token(n, nn)):
            string = strip_from_start(string, substring)
            return True, string, substring, lineno

        else:
            # Error
            substring += gather_invalid_char(string[1:])
            string = strip_from_start(string, substring)
            return False, string, substring, lineno

        return True, string, substring, lineno

    return False, None, None, lineno


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
                    string = strip_from_start(string, substring)
                    return True, string, substring, lineno

                prev = char

            string = strip_from_start(string, substring)
            return False, string, substring, lineno

        if string[1] == "/":
            substring += string[1]
            for char in string[2:]:
                substring += char
                if char == "\n":
                    lineno += 1
                    break

            string = strip_from_start(string, substring)
            return True, string, substring, lineno


    return False, None, None, lineno


def match_keyword(string, substring, lineno):
    if substring in [s[0] for s in KEYWORD]:
        for char in string[1:]:
            substring += char
            if substring in KEYWORD:
                string = strip_from_start(string, substring)
                return True, string, substring, lineno
            if len(substring) > len(max(KEYWORD, key=len)):
                break

    return False, None, None, lineno


def match_id(string, substring, lineno):
    if substring.isalpha():
        for i, char in enumerate(string[1:]):
            if char.isdigit() or char.isalpha():
                substring += char
                continue

            n = string[1:][i + 1] if i + 1 < len(string[1:]) else ""
            if starts_valid_token(char, n):
                string = strip_from_start(string, substring)
                break

            else:
                string = strip_from_start(string, substring)
                second_substring = gather_invalid_char(string)
                string = strip_from_start(string, second_substring)
                return False, string, substring + second_substring, lineno

        return True, string, substring, lineno

    return False, None, None, lineno


def do_matching(string, substring, lineno, token_type, match_function):
    res = match_function(string, substring, lineno)
    success = res[0]
    new_string = res[1]
    matched_string = res[2]
    new_lineno = res[3]
    if success:
        return True, new_string, token_type, matched_string, new_lineno

    elif (not success and matched_string):
        # There was an error -> Report
        report_error(matched_string, new_lineno)
        return True, new_string, None, matched_string, new_lineno

    else:
        # Fall through to next matcher
        return False, None, None, None, None


def match(string, lineno):
    substring = string[0]
    res = do_matching(string, substring, lineno, "whitespace", match_whitespace)
    if res[0]:
        return res[1:]

    res = do_matching(string, substring, lineno, "num", match_num)
    if res[0]:
        return res[1:]

    res = do_matching(string, substring, lineno, "symbol", match_symbol)
    if res[0]:
        return res[1:]

    res = do_matching(string, substring, lineno, "comment", match_comment)
    if res[0]:
        return res[1:]

    res = do_matching(string, substring, lineno, "keyword", match_keyword)
    if res[0]:
        return res[1:]

    res = do_matching(string, substring, lineno, "id", match_id)
    if res[0]:
        return res[1:]

    # Error
    substring += gather_invalid_char(string[1:])
    new_string = strip_from_start(string, substring)
    report_error(substring, lineno)
    return new_string, None, substring, lineno


def write_output(token, substring, lineno, out):
    if not lineno in out:
        out[lineno] = []
    out[lineno].append((token, substring))


def handle_match(token, substring, lineno, symbol_table, out):
    if token == "id":
        symbol_table.append(substring)

    write_output(token, substring, lineno, out)


def get_next_token(data, symbol_table, lineno, out):
    data, token, substring, new_lineno = match(data, lineno)
    if token:
        handle_match(token, substring, lineno, symbol_table, out)
    return data, new_lineno


def main():
    with open("T6/input.txt") as f:
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
