from sly import Parser as SLYParser
import src.AST as AST
from src.scanner import Scanner
from src.utils import get_absolute_path


class Parser(SLYParser):
    tokens = Scanner.tokens

    debugfile = get_absolute_path("data/parser/debug/parser.out")

    precedence = (
        ("nonassoc", "ID"),
        ("nonassoc", "["),
        ("nonassoc", "IFX"),
        ("nonassoc", "ELSE"),
        ("nonassoc", "LE", "GE", "LT", "GT", "EQ", "NEQ", ":"),
        ("left", "+", "DOTPLUS", "-", "DOTMINUS"),
        ("left", "*", "DOTTIMES", "/", "DOTDIVIDE"),
        ("right", "UMINUS", "'"),
    )

    @_("block start", "block")
    def start(self, p):
        if len(p) == 2:
            return AST.Block(p.block, p.start, lineno=p.lineno)
        return AST.Block(p.block, lineno=p.lineno)

    # @_("ID")
    # def expression(self, p):
    #     return AST.Variable(p.ID, lineno=p.lineno)

    @_("assignable")
    def expression(self, p):
        return p.assignable

    @_("STRING")
    def expression(self, p):
        condition = (
            p.STRING[0] == p.STRING[-1] == '"' or p.STRING[0] == p.STRING[-1] == "'"
        )
        parsed_string = p.STRING[1:-1] if condition else p.STRING
        return AST.String(parsed_string, lineno=p.lineno)

    @_("INTNUM")
    def expression(self, p):
        return AST.IntNum(int(p.INTNUM), lineno=p.lineno)

    @_("FLOATNUM")
    def expression(self, p):
        return AST.FloatNum(float(p.FLOATNUM), lineno=p.lineno)

    @_("'(' expression ')'")
    def expression(self, p):
        return p.expression

    @_(
        "expression '+' expression",
        "expression '-' expression",
        "expression '*' expression",
        "expression '/' expression",
        "expression DOTPLUS expression",
        "expression DOTMINUS expression",
        "expression DOTTIMES expression",
        "expression DOTDIVIDE expression",
    )
    def expression(self, p):
        return AST.BinExpr(p[1], p.expression0, p.expression1, lineno=p.lineno)

    @_(
        "expression LT expression",
        "expression GT expression",
        "expression LE expression",
        "expression GE expression",
        "expression NEQ expression",
        "expression EQ expression",
    )
    def expression(self, p):
        return AST.BinExpr(p[1], p.expression0, p.expression1, lineno=p.lineno)

    @_("expression '''")
    def expression(self, p):
        return AST.Transpose(p.expression, lineno=p.lineno)

    @_("'-' expression %prec UMINUS")
    def expression(self, p):
        return AST.BinExpr("-", AST.IntNum(0), p.expression, lineno=p.lineno)

    @_("ZEROS '(' indexes ')' ")
    def expression(self, p):
        return AST.Zeros(p.indexes, lineno=p.lineno)

    @_("ONES '(' indexes ')' ")
    def expression(self, p):
        return AST.Ones(p.indexes, lineno=p.lineno)

    @_("EYE '(' indexes ')'")
    def expression(self, p):
        return AST.Eye(p.indexes, lineno=p.lineno)

    @_("'[' list ']'")
    def expression(self, p):
        return AST.Array(p.list, lineno=p.lineno)

    # @_("ID '[' indexes ']'")
    # def expression(self, p):
    #     return AST.ArrayAccess(
    #         AST.Variable(p.ID, lineno=p.lineno), p.indexes, lineno=p.lineno
    #     ) AST.Array(p.list, lineno=p.lineno)
    @_("list_element ',' spread_elements", "list_element")
    def spread_elements(self, p):
        if len(p) == 1:
            return AST.Spread(p.list_element, lineno=p.lineno)
        return AST.Spread(p.list_element, p.spread_elements, lineno=p.lineno)

    @_("'[' spread_elements ']' ',' list", "'[' spread_elements ']'", "spread_elements")
    def list(self, p):
        if len(p) == 5:
            return AST.Array(p.spread_elements, p.list, lineno=p.lineno)
        return AST.Array(p.spread_elements, lineno=p.lineno)

    @_("INTNUM")
    def list_element(self, p):
        return AST.IntNum(p[0], lineno=p.lineno)

    @_("FLOATNUM")
    def list_element(self, p):
        return AST.FloatNum(p[0], lineno=p.lineno)

    @_("STRING")
    def list_element(self, p):
        condition = (
            p.STRING[0] == p.STRING[-1] == '"' or p.STRING[0] == p.STRING[-1] == "'"
        )
        parsed_string = p.STRING[1:-1] if condition else p.STRING
        return AST.String(parsed_string, lineno=p.lineno)

    @_("ID")
    def list_element(self, p):
        return AST.Variable(p[0], lineno=p.lineno)

    @_("IF '(' expression ')' block ELSE block")
    def statement(self, p):
        return AST.IfElse(
            p.expression, AST.Block(p.block0), AST.Block(p.block1), lineno=p.lineno
        )

    @_("IF '(' expression ')' block %prec IFX")
    def statement(self, p):
        return AST.IfElse(p.expression, AST.Block(p.block), lineno=p.lineno)

    @_("WHILE '(' expression ')' block")
    def statement(self, p):
        return AST.WhileLoop(p.expression, AST.Block(p.block), lineno=p.lineno)

    @_("FOR ID '=' range block")
    def statement(self, p):
        return AST.ForLoop(
            AST.Variable(p.ID), p.range, AST.Block(p.block), lineno=p.lineno
        )

    @_(
        "assignable '=' expression ';'",
        "assignable ADDASSIGN expression ';'",
        "assignable SUBASSIGN expression ';'",
        "assignable MULASSIGN expression ';'",
        "assignable DIVASSIGN expression ';'",
    )
    def statement(self, p):
        return AST.Assignment(p.assignable, p[1], p.expression, lineno=p.lineno)

    @_("RETURN expression ';'")
    def statement(self, p):
        return AST.Return(p.expression, lineno=p.lineno)

    @_("CONTINUE ';'")
    def statement(self, p):
        return AST.Continue(lineno=p.lineno)

    @_("BREAK ';'")
    def statement(self, p):
        return AST.Break(lineno=p.lineno)

    @_("expression ';'")
    def statement(self, p):
        return p.expression

    @_("PRINT prints ';'")
    def statement(self, p):
        return AST.Print(p.prints, lineno=p.lineno)

    @_("statement", "'{' spread_statements '}'")
    def block(self, p):
        if len(p) == 3:
            return AST.Statement(p.spread_statements, lineno=p.lineno)
        return AST.Statement(p.statement, lineno=p.lineno)

    @_("statement spread_statements", "statement")
    def spread_statements(self, p):
        if len(p) == 2:
            return AST.Statement(p.statement, p.spread_statements, lineno=p.lineno)
        return AST.Statement(p.statement, lineno=p.lineno)

    @_("expression ',' prints", "expression")
    def prints(self, p):
        if len(p) == 3:
            return AST.Spread(p.expression, p.prints, lineno=p.lineno)
        else:
            return AST.Spread(p.expression, lineno=p.lineno)

    @_("expression ':' expression")
    def range(self, p):
        # tmp1 = (
        #     AST.IntNum(int(p[0]), lineno=p.lineno)
        #     if p[0].isnumeric()
        #     else AST.Variable(p[0], lineno=p.lineno)
        # )
        # tmp2 = (
        #     AST.IntNum(int(p[2]), lineno=p.lineno)
        #     if p[2].isnumeric()
        #     else AST.Variable(p[2], lineno=p.lineno)
        # )
        return AST.ArrayRange(p.expression0, p.expression1, lineno=p.lineno)

    @_("ID")
    def assignable(self, p):
        return AST.Variable(p.ID, lineno=p.lineno)

    @_("ID '[' indexes ']'")
    def assignable(self, p):
        return AST.ArrayAccess(
            AST.Variable(p.ID, lineno=p.lineno), p.indexes, lineno=p.lineno
        )

    @_("INTNUM ',' indexes", "INTNUM")
    def indexes(self, p):
        if len(p) == 1:
            return [AST.IntNum(int(p[0]), lineno=p.lineno)]
        else:
            return [AST.IntNum(int(p[0]), lineno=p.lineno)] + p.indexes
