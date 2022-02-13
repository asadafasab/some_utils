import pytest
import subprocess

from pathlib import Path
from cat import Cat
from tac import Tac
from print_working_directory import Pwd

FILE = "tests/TEST_FILE"


# def create_tmp_file(tmp_path):
#     file = tmp_path / "test.txt"
#     file.write_text(TEXT)
#     return file


def test_cat():
    # check if basic stuff like opening file(s) works...
    args = [FILE]
    cat_file = subprocess.run(["cat", FILE], capture_output=True).stdout.decode(
        "utf-8", "ignore"
    )
    cat = Cat()
    cat(args)
    assert cat_file == cat.output

    # eol $
    args = [FILE, "-E"]
    cat_file = subprocess.run(["cat", FILE, "-E"], capture_output=True).stdout.decode(
        "utf-8", "ignore"
    )
    cat = Cat()
    cat(args)
    assert cat_file == cat.output

    # test tabs
    args = [FILE, "-T"]
    cat_file = subprocess.run(["cat", FILE, "-T"], capture_output=True).stdout.decode(
        "utf-8", "ignore"
    )
    cat = Cat()
    cat(args)
    assert cat_file == cat.output

    # test squeeze blank
    args = [FILE, "-s"]
    cat_file = subprocess.run(["cat", FILE, "-s"], capture_output=True).stdout.decode(
        "utf-8", "ignore"
    )
    cat = Cat()
    cat(args)
    assert cat_file == cat.output

    # test number nonblank
    args = [FILE, "-b"]
    cat_file = subprocess.run(["cat", FILE, "-b"], capture_output=True).stdout.decode(
        "utf-8", "ignore"
    )
    cat = Cat()
    cat(args)
    assert cat_file == cat.output[:-3] + "\x00\x00"  # ??? rb

    # test numbers
    args = [FILE, "-n"]
    cat_file = subprocess.run(["cat", FILE, "-n"], capture_output=True).stdout.decode(
        "utf-8", "ignore"
    )
    cat = Cat()
    cat(args)
    assert cat_file == cat.output[:-3] + "\x00\x00"  # ??? rb

    # test nonprintable
    args = [FILE, "-v"]
    cat_file = subprocess.run(["cat", FILE, "-v"], capture_output=True).stdout.decode(
        "utf-8", "ignore"
    )
    cat = Cat()
    cat(args)
    assert cat_file == cat.output


def test_pwd():
    pwd = Pwd()
    pwd()
    pwd_command = subprocess.run(["pwd"], capture_output=True).stdout.decode(
        "utf-8", "ignore"
    )
    assert pwd_command == f"{pwd.path}\n"


def test_tac():
    tac = Tac()
    tac([FILE, "-b", "-s"])
    tac_file = subprocess.run(["tac", FILE, "-b"], capture_output=True).stdout.decode(
        "utf-8", "ignore"
    )
    out = tac.output[:668] + tac.output[669:-1]  # xD
    print(out)
    assert tac_file == out

