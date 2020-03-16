"""
Leo Kivikunnas 525925
Jaakko Koskela 526050
"""

from enum import Enum


class SymbolType(Enum):
    KEYWORD = 1
    FUNCTION_INT = 2
    FUNCTION_VOID = 3
    INT = 4
    VOID = 5


class Scanner:
    def __init__(self, filename, symbols, symbol_table, keywords, data):
        self.SYMBOL = symbols
        self.KEYWORD = keywords
        self.lineno = 1
        self.tokens = {}
        # reserve space for type identifier
        self.symbol_table = symbol_table
        self.errors = []
        self.data = data

    def starts_valid_token(self, char):
        if char:
            return (
                char.isspace()
                or char.isdigit()
                or char.isalpha()
                or char in self.SYMBOL
                or char == "/"
            )

        else:
            return True

    def strip_from_start(self, substring):
        self.data = self.data.replace(substring, "", 1)

    def gather_invalid_char(self, string):
        substring = ""
        for i, char in enumerate(string):
            if self.starts_valid_token(char):
                break

            substring += char

        return substring

    def report_error(self, lineno, discarded, reason):
        error_msg = f"{lineno}. ({discarded}, {reason})"
        if "\n" in discarded:
            error_msg = f"{lineno}. ({discarded[:10]}..., {reason})"

        self.errors.append(error_msg)

    def common_error_handler(
        self,
        substring,
        message
    ):
        substring += self.gather_invalid_char(self.data[len(substring):])
        self.strip_from_start(substring)
        if substring == "*/":
            self.report_error(self.lineno, substring, "Unmatched */")
        else:
            self.report_error(self.lineno, substring, message)

        return None, substring

    def match_whitespace(self, substring):
        if substring.isspace():
            if (substring == "\n"):
                self.lineno += 1

            self.strip_from_start(substring)
            return "WHITESPACE", substring

        return None, None

    def match_num(self, substring):
        if substring.isdigit():
            for i, char in enumerate(self.data[1:]):
                if char.isdigit():
                    substring += char

                elif char.isspace() or char in self.SYMBOL or char == "/":
                    break

                else:
                    # Error
                    substring += char
                    return self.common_error_handler(
                        substring,
                        "Invalid number"
                    )

            self.strip_from_start(substring)
            return "NUM", substring

        return None, None

    def match_symbol(self, substring):
        if substring in self.SYMBOL:
            n = self.data[1] if 1 < len(self.data) else None
            if (
                substring != "="
                and substring != "*"
                and substring in self.SYMBOL
            ):
                self.strip_from_start(substring)
                return "SYMBOL", substring

            elif (
                substring == "*"
                and n != "/"
            ):
                self.strip_from_start(substring)
                return "SYMBOL", substring

            elif (substring == "=" and n != "="):
                self.strip_from_start(substring)
                return "SYMBOL", substring

            elif substring == "=" and n == "=":
                substring += n
                self.strip_from_start(substring)
                return "SYMBOL", substring

            else:
                # Error
                if substring == "=" and n == "=":
                    substring += n

                if substring == "*" and n == "/":
                    substring += n
                    self.strip_from_start(substring)
                    self.report_error(self.lineno, substring, "Unmatched */")
                    return None, substring

                return self.common_error_handler(
                    substring,
                    "Invalid symbol"
                )

        return None, None

    def match_comment(self, substring):
        if substring == "/":
            n = self.data[1] if 1 < len(self.data) else None
            substring += n
            if n == "*":
                orig_lineno = self.lineno
                prev = ""
                for char in self.data[2:]:
                    substring += char
                    if char == "\n":
                        self.lineno += 1

                    if prev == "*" and char == "/":
                        self.strip_from_start(substring)
                        return "COMMENT", substring

                    prev = char

                # Error
                self.strip_from_start(substring)
                self.report_error(orig_lineno, substring, "Unclosed comment!")
                return None, substring

            if n == "/":
                for char in self.data[2:]:
                    substring += char
                    if char == "\n":
                        self.lineno += 1
                        break

                self.strip_from_start(substring)
                return "COMMENT", substring

        return None, None

    def match_keyword_or_id(self, substring):
        if substring.isalpha():
            for i, char in enumerate(self.data[1:]):
                if char.isdigit() or char.isalpha():
                    substring += char

                elif self.starts_valid_token(char):
                    self.strip_from_start(substring)
                    if substring in self.KEYWORD:
                        return "KEYWORD", substring

                    return "ID", substring

                else:
                    return self.common_error_handler(
                        substring,
                        "Invalid input"
                    )

            self.strip_from_start(substring)
            if substring in self.KEYWORD:
                return "KEYWORD", substring

            return "ID", substring

        return None, None

    def do_matching(self, substring, match_function):
        res = match_function(substring)
        token_type = res[0]
        matched_string = res[1]
        if token_type:
            return True, token_type, matched_string

        elif (not token_type and matched_string):
            # There was an error
            return True, None, matched_string

        else:
            # Fall through to next matcher
            return False, None, None

    def match(self):
        substring = self.data[0]
        res = self.do_matching(substring, self.match_whitespace)
        if res[0]:
            return res[1:]

        res = self.do_matching(substring, self.match_num)
        if res[0]:
            return res[1:]

        res = self.do_matching(substring, self.match_symbol)
        if res[0]:
            return res[1:]

        res = self.do_matching(substring, self.match_comment)
        if res[0]:
            return res[1:]

        res = self.do_matching(substring, self.match_keyword_or_id)
        if res[0]:
            return res[1:]

        # Error
        return self.common_error_handler(
            substring,
            "Invalid input"
        )

    def save_token(self, token, substring):
        if self.lineno not in self.tokens:
            self.tokens[self.lineno] = []

        self.tokens[self.lineno].append((token, substring))

    def handle_match(self, token, substring):
        if token == "ID" and substring not in self.symbol_table.keys():
            # add new symbol and set type identifier
            self.symbol_table[substring] = {"type": None}
            self.save_token(token, substring)

    def get_next_token(self):
        if not self.data:
            return ("EOF", "$", self.lineno)

        token, substring = self.match()
        if token and token != "COMMENT" and token != "WHITESPACE":
            self.handle_match(token, substring)
            return (token, substring, self.lineno)

        return self.get_next_token()

    def get_type(self, symbol):
        if symbol in self.symbol_table.keys():
            return self.symbol_table[symbol]["type"]
        else:
            # Error: symbol not in symbol table - how to handle?
            return 0

    def write_tokens_to_file(self):
        with open("tokens.txt", "w") as f:
            for key in self.tokens:
                self.tokens[key] = [t for t in self.tokens[key]
                                    if t[0] not in ["WHITESPACE", "COMMENT"]]
                if len(self.tokens[key]) > 0:
                    f.write(f"{key}.")
                    for token in self.tokens[key]:
                        f.write(f" ({token[0]}, {token[1]})")
                    f.write(f"\n")

            f.close()

    def write_symbol_table_to_file(self):
        with open("symbol_table.txt", "w") as f:
            for i, (key, item) in enumerate(self.symbol_table.items()):
                f.write(f"{i + 1}. {key} {item['type']}\n")

            f.close()

    def write_errors_to_file(self):
        with open("lexical_errors.txt", "w") as f:
            if len(self.errors) > 0:
                for i, error in enumerate(self.errors):
                    f.write(f"{error}\n")
            else:
                f.write("There is no lexical errors.")

            f.close()
