import os

from sly import Parser as SLYParser
from src.scanner import Scanner
from src.utils import get_absolute_path


class Parser(SLYParser):
    tokens = Scanner.tokens

    debugfile = get_absolute_path(f"data/parser/debug/parser.out")

    precedence = (
        ("nonassoc", "ADDASSIGN", "SUBASSIGN", "MULASSIGN", "DIVASSIGN"),
        ("nonassoc", "LE", "GE", "LT", "GT", "EQ", "NEQ"),
        ("left", "+", "-", "DOTPLUS", "DOTMINUS"),
        ("left", "*", "/", "DOTTIMES", "DOTDIVIDE"),
        ("right", "\'"),
        ("right", "UMINUS"),
    )

    @_("")
    def empty(self, p):
        pass

    @_("empty")
    def start(self, p):
        pass

    @_("statement start", "'{' start '}' start")
    def start(self, p):
        pass

    @_('INTNUM', 'FLOATNUM', 'STRING')
    def expression(self, p):
        pass

    @_("'(' expression ')' ")
    def expression(self, p):
        pass

    @_("expression '+' expression", "expression '-' expression",
       "expression '*' expression", "expression '/' expression",
       "expression DOTPLUS expression", "expression DOTMINUS expression",
       "expression DOTTIMES expression", "expression DOTDIVIDE expression")
    def expression(self, p):
        pass

    @_("expression LT expression", "expression GT expression",
       "expression LE expression", "expression GE expression",
       "expression NEQ expression", "expression EQ expression",
       "expression '=' expression")
    def expression(self, p):
        pass

    @_("expression '\''")
    def expression(self, p):
        pass

    @_("'-' expression")
    def expression(self, p):
        pass

    @_("ZEROS '(' expression ')' ")
    def expression(self, p):
        pass

    @_("ONES '(' expression ')' ")
    def expression(self, p):
        pass

    @_("EYE '(' expression ')'")
    def expression(self, p):
        pass

    @_("'[' list ']'")
    def expression(self, p):
        pass

    @_("INTNUM", "FLOATNUM", "STRING", "ID", "list")
    def list_element(self, p):
        pass

    @_("spread_elements ',' list_element", "list_element")
    def spread_elements(self, p):
        pass

    @_("list ',' '[' spread_elements ']'", "'[' spread_elements ']'")
    def list(self, p):
        pass

    @_("ID", "ID '[' indexes ']'")
    def assignable(self, p):
        pass

    @_("INTNUM ',' indexes", "INTNUM")
    def indexes(self, p):
        pass

    @_("assignable '=' expression ';'", "assignable ADDASSIGN expression ';'",
       "assignable SUBASSIGN expression ';'", "assignable MULASSIGN expression ';'",
       "assignable DIVASSIGN expression ';'", "RETURN expression ';'", "CONTINUE ';'",
       "BREAK ';'", "expression ';'", "PRINT prints ';'", "IF expression block",
       "IF expression block ELSE block", "WHILE expression block", "FOR ID '=' range block"
       )
    def statement(self, p):
        pass

    @_("statement", "'{' start '}'")
    def block(self, p):
        pass

    @_("expression ',' prints", "expression ';'")
    def prints(self, p):
        pass

    @_('INTNUM ":" INTNUM', 'ID ":" ID', 'ID ":" INTNUM', 'INTNUM ":" ID')
    def range(self, p):
        pass


