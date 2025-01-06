import sys

from src.TypeChecker import TypeChecker
from src.parser import Parser
from src.scanner import Scanner
from src.utils import get_absolute_path
from tree_printer import TreePrinter


def main():
    default = ("tc", "opers.m")
    lab = sys.argv[1] if len(sys.argv) == 3 else default[0]
    file_name = sys.argv[2] if len(sys.argv) == 3 else default[1]
    path = get_absolute_path(f"data/{lab}/{file_name}")
    try:
        file = open(path, "r")
    except IOError:
        print(f"Cannot open file under path: {path}")
        sys.exit(0)
    text = file.read()
    match lab:
        case "parser":
            test_parser(text)
        case "scanner":
            test_scanner(text)
        case "ast":
            test_ast(text)
        case "tc":
            test_type_checker(text)


def test_ast(text):
    lexer = Scanner()
    parser = Parser()
    ast = parser.parse(lexer.tokenize(text))
    ast.printTree()


def test_parser(text):
    lexer = Scanner()
    parser = Parser()
    parser.parse(lexer.tokenize(text))


def test_scanner(text):
    lexer = Scanner()
    for tok in lexer.tokenize(text):
        print(tok)

def test_type_checker(text):
    lexer = Scanner()
    parser = Parser()
    ast = parser.parse(lexer.tokenize(text))
    tc = TypeChecker()
    tc.visit(ast)



if __name__ == "__main__":
    main()
