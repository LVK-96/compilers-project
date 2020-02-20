import sys
from scanner import Scanner


def main(argv):
    filename = "input.txt"
    # TODO: Remove this before turn in
    if argv and argv[0]:
        filename = argv[0]

    s = Scanner(filename)
    while True:
        token = s.get_next_token()
        if token[1] == "$":
            break

    s.write_tokens_to_file()
    s.write_symbol_table_to_file()
    s.write_errors_to_file()


if __name__ == "__main__":
    argv = sys.argv[1:]
    main(argv)
