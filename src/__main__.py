import sys
import os

from src.scanner import Scanner


def main():
    file = load_file()
    text = file.read()
    lexer = Scanner()

    for tok in lexer.tokenize(text):
        print(tok)

def load_file():
    script_dir = os.path.dirname(__file__)  # <-- absolute dir the script is in
    path = os.path.normpath(script_dir)
    path = path.split(os.sep)
    path.pop()
    path.append("data")
    path = os.sep.join(path)
    filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
    path = os.path.join(path, filename)
    try:
        file = open(path, "r")
    except IOError:
        print("Cannot open {0} file".format(path))
        sys.exit(0)
    return file

if __name__ == "__main__":
    main()