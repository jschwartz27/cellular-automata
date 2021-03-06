import os
import sys
import time
import random
import argparse

'''
excellent rules to checkout are:
    22
    154
    225
'''


def error_and_exit(msg: str) -> None:
    sys.stderr.write("\nError: {}\n".format(msg))
    sys.exit(1)


def arg_check() -> object:

    def str2bool(v) -> bool:
        if isinstance(v, bool):
            return v
        if v.lower() in ('yes', 'true', 't', 'y', '1'):
            return True
        elif v.lower() in ('no', 'false', 'f', 'n', '0'):
            return False
        else:
            raise argparse.ArgumentTypeError('Boolean value expected.')

    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--seed", type=str2bool, nargs='?',
                        const=True, default=False,
                        help="Seed or randomized first level")
    parser.add_argument("-r", "--rule", required=False, type=int,
                        choices=range(256),
                        default=random.randrange(256),
                        help="Would you care for a particular rule?")
    parser.add_argument("-v", "--symbol_value", required=False, type=str,
                        default="?",
                        help="Default symbol for the cellular automata?")

    # this will cause changes in rule every 100 or whatever iterations
    # parser.add_argument("--randomize", type=str2bool, nargs='?',
    #                     const=True, default=False,
    #                     help="Seed or randomized first level")

    # ap.add_argument("-c", "--class", required=False,
    #                help="A randomized selection from a give class (1-4)")

    return vars(parser.parse_args())


class CellularAutomata:

    terminal_length = os.get_terminal_size().columns - 1
    # 111 110 101 100 011 010 001 000
    states = ['{0:03b}'.format(k) for k in range(8)][::-1]
    sleep_time = 0.025

    def __init__(self, args):
        self.SYMBOL = args["symbol_value"]
        # convert rule number from decimal to binary
        self.n_binary = '{0:08b}'.format(args["rule"])
        self.transition_rules = {self.states[i]: self.n_binary[i] for i in range(8)}
        self.create(args["rule"], args["seed"])

    @staticmethod
    def conv(x: str) -> str:
        return "0" if x == " " else "1"

    def conv_binary(self, x: str) -> str:
        return self.SYMBOL if x == "1" else " "

    def create(self, rule: str, seed: bool) -> None:
        print("\nRule Number :: {}".format(rule))
        print("Binary      :: {}\n".format(self.n_binary))
        time.sleep(1)

        if seed:
            last_row = [" "] * (self.terminal_length - 1) + [self.SYMBOL]
        else:
            last_row = list(map(
                lambda x: random.choice([self.SYMBOL, " "]), range(self.terminal_length)))

        the_structure = [last_row]
        for _ in range(10000):
            print("".join(last_row))
            time.sleep(self.sleep_time)
            # because the index for loop can't wrap around
            q = last_row[-1:] + last_row[:2]
            q = "".join(list(map(lambda x: self.conv(x), q)))
            next_row = [self.conv_binary(self.transition_rules[q])]

            for j in range(1, self.terminal_length-1):
                q = "".join(list(map(lambda x: self.conv(x), last_row[j-1:j+2])))
                next_row.append(self.conv_binary(self.transition_rules[q]))

            # because the index for loop can't wrap around
            q = last_row[-2:] + last_row[:1]
            v = "".join(list(map(lambda x: self.conv(x), q)))
            next_row.append(self.conv_binary(self.transition_rules[v]))
            last_row = next_row
            the_structure.append(last_row)


def main():
    CellularAutomata(arg_check())


if __name__ == '__main__':
    main()
