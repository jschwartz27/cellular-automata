import os
import sys
import time
import random
import argparse
from typing import List

SYMBOL = "?"


def error_and_exit(msg: str) -> None:
    sys.stderr.write("\nError: {}\n".format(msg))
    sys.exit(1)


def arg_check() -> object:
    ap = argparse.ArgumentParser()
    ap.add_argument("-s", "--seed", required=True, type=bool,
                    help="Seed or randomized first level")
    ap.add_argument("-r", "--rule", required=False, type=int,
                    choices=range(256),
                    help="Would you care for a particular rule?")
    # ap.add_argument("-c", "--class", required=False,
    #                help="A randomized selection from a give class (1-4)")
    args = vars(ap.parse_args())

    if not args["rule"]:
        args["rule"] = random.randrange(256)

    return args


def conv(x):
    return "0" if x == " " else "1"


def conv_binary(x):
    return SYMBOL if x == "1" else " "


def automata(transition_rules, seed: bool) -> List[List[str]]:
    terminal_length = os.get_terminal_size().columns - 1

    if seed:
        cell = [" "] * (terminal_length - 1) + [SYMBOL]
    else:
        cell = list(map(
            lambda x: random.choice([SYMBOL, " "]), range(terminal_length)))

    it = [cell]
    for i in range(10000):
        print("".join(cell))
        time.sleep(.05)
        next_row = list()
        # because the index for loop can't wrap around
        q = cell[-1:] + cell[:2]
        q = "".join(list(map(lambda x: conv(x), q)))
        k = conv_binary(transition_rules[q])
        next_row.append(k)

        for j in range(1, terminal_length-1):
            q = cell[j-1:j+2]
            q = "".join(list(map(lambda x: conv(x), q)))
            k = conv_binary(transition_rules[q])
            next_row.append(k)
        # because the index for loop can't wrap around
        q = cell[-2:] + cell[:1]
        q = "".join(list(map(lambda x: conv(x), q)))
        k = conv_binary(transition_rules[q])
        next_row.append(k)

        cell = next_row
        it.append(cell)

    return it


def main():
    args = arg_check()
    # convert rule number from decimal to binary
    n_binary = '{0:08b}'.format(args["rule"])

    print("\nRule Number :: {}".format(args["rule"]))
    print("Binary      :: {}\n".format(n_binary))

    # 111 110 101 100 011 010 001 000
    states = ['{0:03b}'.format(k) for k in range(8)][::-1]
    # transition rules
    transition_rules = {states[i]: n_binary[i] for i in range(8)}
    the_structure = automata(transition_rules, args["seed"])


if __name__ == '__main__':
    main()
