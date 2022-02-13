import argparse
import os

parser = argparse.ArgumentParser(description="pwd...")
parser.add_argument("dir", metavar="file", type=str)
# parser.add_argument("-L", help="", action="store_true")
# parser.add_argument("-P", help="", action="store_true")
# parser.add_argument("-e", help="", action="store_true")


class Cd:
    def __init__(self, args):
        ...

    def __call__(self, args):
        os.chdir(args.dir)


if __name__ == "__main__":
    cd = Cd()
    cd(parser.parse_args())
