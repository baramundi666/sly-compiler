import sys

from src.interpreter import Interpreter
from src.type_checker import TypeChecker, ErrorType
from src.parser import Parser
from src.scanner import Scanner
from src.utils import get_absolute_path
from src.tree_printer import TreePrinter


def main():
    default = ("interpreter", "matrix.m")
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
        case "interpreter":
            test_interpreter(text)
        case _:
            print(f"Invalid lab argument: {lab}")

def test_interpreter(text):
    lexer = Scanner()
    parser = Parser()
    ast = parser.parse(lexer.tokenize(text))
    tc = TypeChecker()
    tc_result = tc.visit(ast)
    if isinstance(tc_result, ErrorType):
        raise RuntimeError("Type checker error")
    interpreter = Interpreter()
    interpreter.visit(ast)

def test_type_checker(text):
    lexer = Scanner()
    parser = Parser()
    ast = parser.parse(lexer.tokenize(text))
    tc = TypeChecker()
    tc.visit(ast)

def test_ast(text):
    lexer = Scanner()
    parser = Parser()
    ast = parser.parse(lexer.tokenize(text))
    TreePrinter()
    ast.printTree()

def test_parser(text):
    lexer = Scanner()
    parser = Parser()
    parser.parse(lexer.tokenize(text))

def test_scanner(text):
    lexer = Scanner()
    for tok in lexer.tokenize(text):
        print(tok)


if __name__ == "__main__":
    main()
