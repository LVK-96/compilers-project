symbols = ["=", ";", ":", ",", "[", "]", "(", ")", "{", "}",
           "+", "-", "*", "=", "<", "=="]
keywords = ["if", "else", "void", "int", "while", "break",
            "continue", "switch", "default", "case", "return"]
terminals = ["ID", "NUM"] + symbols + keywords


def first_of(production, productions, first_calculated, firsts):
    if first_calculated[production[0]]:
        return firsts[production[0]]

    for p in production[1]:
        elems = p.split(" ")
        if (elems[0] == "EPSILON" and len(elems) == 1):
            firsts[production[0]].append(elems[0])

        elif elems[0] in terminals:
            firsts[production[0]].append(elems[0])

        else:
            first_of_other = first_of((elems[0], productions[elems[0]]), productions, first_calculated, firsts)
            firsts[production[0]] += first_of_other

    firsts[production[0]] = list(set(firsts[production[0]]))
    first_calculated[production[0]] = True
    return firsts[production[0]]


def follow_of(non_terminal, productions, firsts, follow_calculated, follows):
    if follow_calculated[non_terminal]:
        return follows[non_terminal]

    for k, p in productions.items():
        for sub in p:
            elems = sub.split(" ")
            if non_terminal in elems:
                i = elems.index(non_terminal)
                if i < len(elems) - 1:
                    n = elems[i + 1]
                    if n in terminals:
                        follows[non_terminal].append(n)
                    else:
                        follows[non_terminal] += firsts[n]
                else:
                    if k != p:
                        follows[non_terminal] += follow_of(k, productions, firsts, follow_calculated, follows)

    follow_calculated[non_terminal] = True
    follows[non_terminal] = list(set(follows[non_terminal]))
    return follows[non_terminal]


def main():
    with open("grammar.txt") as f:
        data = f.read()
        data = data.rstrip()
        f.close

    data = data.split("\n")
    productions = {}
    first_calculated = {}
    firsts = {}
    follow_calculated = {}
    follows = {}
    for p in data:
        lhs_rhs = p.split(" -> ")
        lhs = lhs_rhs[0]
        first_calculated[lhs] = False
        firsts[lhs] = []
        productions[lhs] = []
        follow_calculated[lhs] = False
        follows[lhs] = []
        rhs = lhs_rhs[1]
        rhs = rhs.split(" | ")
        for r in rhs:
            productions[lhs].append(r)

    for p in productions:
        first_of((p, productions[p]), productions, first_calculated, firsts)


    follows["Program"].append("$")
    while True:
        changed = False
        for k, p in productions.items():
            for sub in p:
                elems = sub.split(" ")
                for elem in elems:
                    if elem in terminals + ["EPSILON"]:
                        continue

                    orig_size = len(follows[elem])
                    rest = elems[elems.index(elem) + 1::]
                    if len(rest) > 0:
                        if rest[0] not in terminals:
                            if "EPSILON" not in firsts[rest[0]]:
                                follows[elem] += firsts[rest[0]]
                            else:
                                follows[elem] += firsts[rest[0]]
                                follows[elem].remove("EPSILON")
                                follows[elem] += follows[rest[0]]

                        else:
                            follows[elem].append(rest[0])
                    else:
                        follows[elem] += follows[k]

                    follows[elem] = list(set(follows[elem]))
                    if len(follows[elem]) > orig_size:
                        changed = True

        if not changed:
            break

    print("First")
    for f in firsts:
        print(f, firsts[f])

    print()
    print("Follow")
    for f in follows:
        print(f, follows[f])

if __name__ == "__main__":
    main()
