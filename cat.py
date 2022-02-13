import argparse
from typing import List
from utils import m_miunus_notation

READ_ONLY_MODE = "r"
READ_ONLY_BINARY_MODE = "rb"

parser = argparse.ArgumentParser(description="Cat...")
parser.add_argument("files", metavar="file", type=str, nargs="+")
# parser.add_argument("-A", "--show-all", action="store_true")
# parser.add_argument("-e", action="store_true", help="")
# parser.add_argument("-t", action="store_true")
parser.add_argument(
    "-b", "--number-nonblank", help="number nonempty output lines", action="store_true",
)
parser.add_argument(
    "-E", "--show-ends", action="store_true", help="display $ at end of each line",
)
parser.add_argument(
    "-n", "--number", action="store_true", help="number all output lines"
)
parser.add_argument(
    "-s",
    "--squeeze-blank",
    action="store_true",
    help="suppress repeated empty output lines",
)
parser.add_argument(
    "-T", "--show-tabs", action="store_true", help="display TAB characters as ^I",
)
parser.add_argument(
    "-v",
    "--show-nonprinting",
    action="store_true",
    help="use ^ and M- notation, except for LFD and TAB",
)


class Cat:
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
        if mode == READ_ONLY_MODE:
            with open(file, mode, errors="ignore") as f:
                return f.read()
        elif mode == READ_ONLY_BINARY_MODE:
            with open(file, mode) as f:
                return f.read()

    def append_ends(self) -> None:
        self.output = self.output.replace("\n", "$\n")

    def show_tabs(self) -> None:
        self.output = self.output.replace("\t", "^I")

    def show_nonprinting(self) -> None:
        out = ""
        char = ""
        text_memory = memoryview(self.output)
        for i, number in enumerate(text_memory):
            char = m_miunus_notation(str(number))
            if char == str(number):
                char = chr(number)
            out += char
        self.output = out

    def show_numbers(self) -> None:
        out = ""
        text = self.output.split("\n")
        text_spacing = len(str(len(text))) + 4

        for num, line in enumerate(text):
            spacing = " " * (text_spacing - len(str(num + 1)))
            out += f"{spacing}{num+1}\t{line}\n"

        self.output = out

    def squeeze_blank(self) -> None:
        out = ""
        skiped = 0
        for line in self.output.split("\n"):
            if line == "":
                skiped += 1
            else:
                if skiped > 1:
                    out += f"\n{line}\n"
                else:
                    out += f"{line}\n"
                skiped = 0
        if out[-1] == "\n":
            self.output = out[:-1]
        else:
            self.output = out

    def show_number_nonblank(self) -> None:
        out = ""
        num = 0
        text = self.output.split("\n")
        text_spacing = len(str(len(text))) + 4

        for line in text:
            if line == "":
                out += f"\n"
            else:
                num += 1
                spacing = " " * (text_spacing - len(str(num)))
                out += f"{spacing}{num}\t{line}\n"

        self.output = out

    def prepare_output(self, args) -> None:
        mode = READ_ONLY_MODE
        self.output = ""
        if args.show_nonprinting:
            mode = READ_ONLY_BINARY_MODE
            self.output = b""

        for f in args.files:
            self.output += self.open_file(f, mode)

        if args.show_ends:
            self.append_ends()
        if args.show_tabs:
            self.show_tabs()
        if args.number and not args.number_nonblank:
            self.show_numbers()
        if args.show_nonprinting:
            self.show_nonprinting()
        if args.squeeze_blank:
            self.squeeze_blank()
        if args.number_nonblank:
            self.show_number_nonblank()


if __name__ == "__main__":
    cat = Cat()
    cat()
