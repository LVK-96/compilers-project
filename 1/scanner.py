"""
Leo Kivikunnas 525925
Jaakko Koskela 526050
"""


import sys # TODO: Remove this before turn in


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


def gather_invalid_char(string):
    substring = ""
    for i, char in enumerate(string):
        n = string[i + 1] if i + 1 < len(string) else None
        if starts_valid_token(char, n):
            break

        substring += char

    return substring


def report_error(discarded, lineno, reason, errors):
    error_msg = f"{lineno}. ({discarded}, {reason})"
    if "\n" in discarded:
        error_msg = f"{lineno}. ({discarded[:10]}..., {reason})"

    errors.append(error_msg)


def match_whitespace(string, substring, lineno, errors):
    if substring.isspace():
        if (substring == "\n"):
            lineno += 1

        string = strip_from_start(string, substring)
        return "WHITESPACE", string, substring, lineno

    return None, None, None, lineno


def match_num(string, substring, lineno, errors):
    if substring.isdigit():
        for char in string[1:]:
            if char.isdigit():
                substring += char

            elif char in SYMBOL or char.isspace():
                break

            else:
                # Error
                substring += char
                substring += gather_invalid_char(string[len(substring):])
                string = strip_from_start(string, substring)
                if substring[:2] == "*/":
                    report_error(substring, lineno, "Unmatched */", errors)
                else:
                    report_error(substring, lineno, "Invalid number", errors)
                return None, string, substring, lineno

        string = strip_from_start(string, substring)
        return "NUM", string, substring, lineno

    return None, None, None, lineno


def match_symbol(string, substring, lineno, errors):
    if substring in SYMBOL:
        n = string[1] if 1 < len(string) else None
        nn = string[2] if 2 < len(string) else None
        nnn = string[3] if 3 < len(string) else None
        if substring != "=" and substring in SYMBOL and starts_valid_token(n, nn):
            string = strip_from_start(string, substring)
            return "SYMBOL", string, substring, lineno

        elif (substring == "=" and n != "=" and starts_valid_token(n, nn)):
            string = strip_from_start(string, substring)
            return "SYMBOL", string, substring, lineno

        elif substring == "=" and n == "=" and starts_valid_token(nn, nnn):
            substring += n
            string = strip_from_start(string, substring)
            return "SYMBOL", string, substring, lineno

        else:
            # Error
            if substring == "=" and n == "=":
                substring += n
            substring += gather_invalid_char(string[len(substring):])
            string = strip_from_start(string, substring)
            if substring[:2] == "*/":
                report_error(substring, lineno, "Unmatched */", errors)
            else:
                report_error(substring, lineno, "Invalid symbol", errors)
            return None, string, substring, lineno

    return None, None, None, lineno


def match_comment(string, substring, lineno, errors):
    if substring == "/":
        n = string[1] if 1 < len(string) else None
        substring += n
        if n == "*":
            orig_lineno = lineno
            prev = ""
            for char in string[2:]:
                substring += char
                if char == "\n":
                    lineno += 1

                if prev == "*" and char == "/":
                    string = strip_from_start(string, substring)
                    return "COMMENT", string, substring, lineno

                prev = char

            # Error
            string = strip_from_start(string, substring)
            report_error(substring, orig_lineno, "Unclosed comment!", errors)
            return None, string, substring, lineno

        if n == "/":
            for char in string[2:]:
                substring += char
                if char == "\n":
                    lineno += 1
                    break

            string = strip_from_start(string, substring)
            return "COMMENT", string, substring, lineno


    return None, None, None, lineno


def match_id(string, substring, lineno, errors, carry_over=None):
    for i, char in enumerate(string[1:]):
        n = string[1:][i + 1] if i + 1 < len(string[1:]) else None
        if char.isdigit() or char.isalpha():
            substring += char

        elif starts_valid_token(char, n):
            string = strip_from_start(string, substring)
            return "ID", string, substring, lineno

        else:
            # Error
            substring += gather_invalid_char(string[len(substring):])
            string = strip_from_start(string, substring)
            if (carry_over):
                substring = carry_over + substring

            if substring[:2] == "*/":
                report_error(substring, lineno, "Unmatched */", errors)
            else:
                report_error(substring, lineno, "Invalid input", errors)

            return None, string, substring, lineno

    return None, None, None, lineno


def match_keyword(string, substring, lineno, errors):
    for i, char in enumerate(string[1:]):
        n = string[1:][i + 1] if i + 1 < len(string[1:]) else None
        substring += char
        keyword_starts = [s[:len(substring)] for s in KEYWORD]
        if substring in KEYWORD:
            string = strip_from_start(string, substring)
            return "KEYWORD", string, substring, lineno

        elif substring in keyword_starts:
            continue

        elif (char.isalpha() or char.isdigit()) and substring not in keyword_starts:
            # It might be an id instead
            string = strip_from_start(string, substring[:-1])
            res = match_id(string, substring[-1], lineno, errors, substring[:-1])
            substring = substring[:-1] + res[2]
            return res[:2] + (substring, ) + res[3:]

        elif starts_valid_token(char, n):
            # It is an id
            string = strip_from_start(string, substring[:-1])
            return "ID", string, substring[:-1], lineno

        else:
            # Error
            substring += gather_invalid_char(string[len(substring):])
            string = strip_from_start(string, substring)
            if substring[:2] == "*/":
                report_error(substring, lineno, "Unmatched */", errors)
            else:
                report_error(substring, lineno, "Invalid input", errors)
            return None, string, substring, lineno

    return None, None, None, lineno


def match_keyword_or_id(string, substring, lineno, errors):
    if substring in [s[0] for s in KEYWORD]:
        return match_keyword(string, substring, lineno, errors)

    elif substring.isalpha():
        return match_id(string, substring, lineno, errors)

    return None, None, None, lineno


def do_matching(string, substring, lineno, match_function, errors):
    # All matching function return (token_type, new_string, matched_string, new_lineno)
    res = match_function(string, substring, lineno, errors)
    token_type = res[0]
    new_string = res[1]
    matched_string = res[2]
    new_lineno = res[3]
    if token_type:
        return True, new_string, token_type, matched_string, new_lineno

    elif (not token_type and matched_string):
        # There was an error -> Report
        return True, new_string, None, matched_string, new_lineno

    else:
        # Fall through to next matcher
        return False, None, None, None, None


def match(string, lineno, errors):
    substring = string[0]
    res = do_matching(string, substring, lineno, match_whitespace, errors)
    if res[0]:
        return res[1:]

    res = do_matching(string, substring, lineno, match_num, errors)
    if res[0]:
        return res[1:]

    res = do_matching(string, substring, lineno, match_symbol, errors)
    if res[0]:
        return res[1:]

    res = do_matching(string, substring, lineno, match_comment, errors)
    if res[0]:
        return res[1:]

    res = do_matching(string, substring, lineno, match_keyword_or_id, errors)
    if res[0]:
        return res[1:]

    # Error
    substring += gather_invalid_char(string[1:])
    new_string = strip_from_start(string, substring)
    report_error(substring, lineno, "Invalid input", errors)
    return new_string, None, substring, lineno


def save_token(token, substring, lineno, tokens):
    if not lineno in tokens:
        tokens[lineno] = []
    tokens[lineno].append((token, substring))


def handle_match(token, substring, lineno, tokens, symbol_table):
    if token == "ID" and substring not in symbol_table:
        symbol_table.append(substring)

    save_token(token, substring, lineno, tokens)


def get_next_token(data, lineno, tokens, symbol_table, errors):
    data, token, substring, new_lineno = match(data, lineno, errors)
    if token:
        handle_match(token, substring, lineno, tokens, symbol_table)
    return data, new_lineno


def write_tokens_to_file(tokens):
    with open("tokens.txt", "w") as f:
        for key in tokens:
            tokens[key] = [t for t in tokens[key] if t[0] not in ["WHITESPACE", "COMMENT"]]
            if len(tokens[key]) > 0:
                f.write(f"{key}.")
                for token in tokens[key]:
                    f.write(f" ({token[0]}, {token[1]})")
                f.write(f"\n")

        f.close()

def write_symbol_table_to_file(symbol_table):
    with open("symbol_table.txt", "w") as f:
        for i, symbol in enumerate(symbol_table):
            f.write(f"{i + 1}. {symbol}\n")

        f.close()


def write_errors_to_file(errors):
    with open("lexical_errors.txt", "w") as f:
        if len(errors) > 0:
            for i, error in enumerate(errors):
                f.write(f"{error}\n")
        else:
            f.write("There is no lexical errors.")

        f.close()


def debug_prints(tokens, symbol_table, errors):
    print("\nTokens:")
    tokens_print = {}
    for key in tokens:
        if len(tokens[key]) > 0:
            print(tokens[key])

    symbol_table_print = list(dict.fromkeys(symbol_table))
    print("\nSymbol table:")
    print(symbol_table_print)

    errors_print = list(dict.fromkeys(errors))
    print("\nErrors:")
    print(errors_print)


def main(argv):
    filename = "input.txt"

    # TODO: Remove this before turn in
    if argv and argv[0]:
        filename = argv[0]

    with open(filename) as f:
        data = f.read()
        data = data.rstrip("\n")
        f.close()

    lineno = 1
    tokens = {}
    symbol_table = ["if", "else", "void", "int", "while", "break", "continue",
                    "switch", "default", "case", "return"]
    errors = []
    while data:
        data, lineno = get_next_token(data, lineno, tokens, symbol_table, errors)

    debug_prints(tokens, symbol_table, errors) # TODO: delete this before turn in

    write_tokens_to_file(tokens)
    write_symbol_table_to_file(symbol_table)
    write_errors_to_file(errors)


if __name__ == "__main__":
    argv = sys.argv[1:]
    main(argv)
