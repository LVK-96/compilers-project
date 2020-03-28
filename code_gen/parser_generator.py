import sys
import json

symbols = [";", ":", ",", "[", "]", "(", ")", "{", "}",
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
            first_of_other = []
            i = 0
            while i < len(elems):
                first_of_other += first_of((elems[i],
                                            productions[elems[i]]),
                                           productions,
                                           first_calculated,
                                           firsts)
                i += 1
                if "EPSILON" not in first_of_other:
                    break

            firsts[production[0]] += first_of_other

    firsts[production[0]] = list(set(firsts[production[0]]))
    first_calculated[production[0]] = True
    return firsts[production[0]]


def make_firsts(productions, first_calculated, firsts):
    for p in productions:
        first_of((p, productions[p]), productions, first_calculated, firsts)

    return firsts


def make_follows(follows, productions, firsts):
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

    return follows


def make_table(
        firsts,
        follows,
        productions,
        productions_without_action_symbols):
    ll1_table = []
    terminals_with_eof = terminals + ["$"]
    for f in firsts:
        line = [None] * len(terminals_with_eof)
        for t in terminals_with_eof:
            if t in firsts[f]:
                correct_production = None
                for p in productions_without_action_symbols[f]:
                    elems = p.split(" ")
                    if elems[0] == t:
                        correct_production = productions[f][productions_without_action_symbols[f].index(
                            p)]
                        break

                    i = 0
                    while i < len(elems):
                        if elems[i] in firsts:
                            if t in firsts[elems[i]]:
                                correct_production = productions[f][productions_without_action_symbols[f].index(
                                    p)]
                                break

                            if "EPSILON" not in firsts[elems[i]]:
                                break

                        elif elems[i] in terminals_with_eof:
                            break

                        i += 1

                line[terminals_with_eof.index(t)] = correct_production

        if "EPSILON" in firsts[f]:
            for t in terminals_with_eof:
                if t in follows[f]:
                    correct_production = None
                    for p in productions_without_action_symbols[f]:
                        elems = p.split(" ")
                        if elems[0] == "EPSILON":
                            correct_production = productions[f][productions_without_action_symbols[f].index(
                                p)]
                            break
                        elif elems[0] in firsts and "EPSILON" in firsts[elems[0]]:
                            correct_production = productions[f][productions_without_action_symbols[f].index(
                                p)]
                            break

                    line[terminals_with_eof.index(t)] = correct_production

        for t in terminals_with_eof:
            if t in follows[f] and not line[terminals_with_eof.index(t)]:
                correct_production = "SYNCH"
                line[terminals_with_eof.index(t)] = correct_production

        ll1_table.append(line)

    return ll1_table


def debug_print(firsts, follows, table):
    print("Firsts")
    for f in firsts:
        print(f, firsts[f])

    print()
    print("Follows")
    for f in follows:
        print(f, follows[f])

    print()
    for line in table:
        print(line)


def gen_table(argv):
    filename = "grammar.txt"
    if len(argv) > 0:
        filename = argv[0]
    with open(filename) as f:
        data = f.read()
        data = data.rstrip()
        f.close

    data = data.split("\n")
    productions = {}
    productions_without_action_symbols = {}
    first_calculated = {}
    firsts = {}
    follows = {}
    for p in data:
        lhs_rhs = p.split(" -> ")
        lhs = lhs_rhs[0]
        first_calculated[lhs] = False
        firsts[lhs] = []
        productions[lhs] = []
        follows[lhs] = []
        rhs = lhs_rhs[1]
        rhs = rhs.split(" | ")
        for r in rhs:
            productions[lhs].append(r)

    for p in productions:
        new_sub = []
        for sub in productions[p]:
            elems = [e for e in sub.split(" ") if not e.startswith("#")]
            without_action_symbols = " ".join(elems)
            new_sub.append(without_action_symbols)
        productions_without_action_symbols[p] = new_sub

    firsts = make_firsts(productions_without_action_symbols,
                         first_calculated, firsts)
    follows = make_follows(follows, productions_without_action_symbols, firsts)
    ll1_table = make_table(firsts, follows, productions,
                           productions_without_action_symbols)

    # debug_print(firsts, follows, ll1_table)

    with open('table.txt', 'w') as f:
        for line in ll1_table:
            f.write("%s,\n" % line)

        f.close()

    with open('firsts.json', 'w') as f:
        json_string = json.dumps(firsts)
        f.write(json_string)
        f.close()

    with open('follows.json', 'w') as f:
        json_string = json.dumps(follows)
        f.write(json_string)
        f.close()

    return ll1_table


if __name__ == "__main__":
    argv = sys.argv[1:]
    gen_table(argv)
