import argparse
from typing import List


READ_ONLY_MODE = "r"
READ_ONLY_BINARY_MODE = "rb"

parser = argparse.ArgumentParser(description="taC")
parser.add_argument("files", type=str, nargs="+", help="...")
parser.add_argument(
    "-b",
    "--before",
    help="attach the separator before instead of after",
    action="store_true",
)
parser.add_argument(
    "-s",
    "--separator",
    help="use STRING as the separator instead of newline",
    action="store_const",
    const="\n",
)


class Tac:
    def __init__(self):
        self.output = ""

    def __call__(self, arguments: List = []):
        if arguments:
            args = parser.parse_args(arguments)
        else:
            args = parser.parse_args()
        self.prepare_output(args)
        print(self.output)

    def open_file(self, file: str, mode: str) -> str:
        with open(file, mode, errors="ignore") as f:
            text: List = f.read()
        text = text.split("\n")[::-1]
        for i in range(len(text)):
            text[i] += "\n"

        return "".join(text)

    def prepare_output(self, args) -> None:
        separator = args.separator
        if args.separator == None:
            separator = "\n"

        for f in args.files:
            self.output += self.open_file(f, READ_ONLY_MODE)
            if args.before:
                self.output = separator + self.output
