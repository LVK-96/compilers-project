"""
Compare two files (case-insensitive and doesnt take into account whitespace
Usage: are_contents_equal file1 file2
"""

import sys


def main(file_name1, file_name2):
    with open(file_name1) as f1:
        data1 = f1.read()
        f1.close()

    with open(file_name2) as f2:
        data2 = f2.read()
        f2.close()

    formatted_data1 = "".join(data1.split()).lower()
    formatted_data2 = "".join(data2.split()).lower()


    if formatted_data1 == formatted_data2:
        print("OK")
        return 0

    print("Difference found!")
    print(data1)
    print()
    print(data2)

    index = next((i for i, (char1, char2) in enumerate(zip(formatted_data1, formatted_data2)) if char1 != char2), None)
    if index:
        print()
        print(formatted_data1[index], f"difference at {index}")

    return 1


if __name__== "__main__":
    argv = sys.argv[1:]
    main(argv[0], argv[1])


