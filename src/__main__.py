import sys
import os
from ast import Param

from src.parser import Parser
from src.scanner import Scanner


def main():
    file = load_file("parser")
    text = file.read()

    lexer = Scanner()
    parser = Parser()

    parser.parse(lexer.tokenize(text))


def load_file(dir: str):
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    path = os.path.normpath(script_dir)
    path = path.split(os.sep)
    path.pop()
    path.append("data/" + dir)
    path = os.sep.join(path)
    filename = sys.argv[1] if len(sys.argv) > 1 else "example1.m"
    path = os.path.join(path, filename)
    try:
        file = open(path, "r")
    except IOError:
        print("Cannot open {0} file".format(path))
        sys.exit(0)
    return file


if __name__ == "__main__":
    main()
