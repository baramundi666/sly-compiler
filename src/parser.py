from sly import Parser as SLYParser
from src import AST
from src.scanner import Scanner
from src.utils import get_absolute_path


class Parser(SLYParser):
    tokens = Scanner.tokens

    debugfile = get_absolute_path("data/parser/debug/parser.out")

    precedence = (
        ("nonassoc", "IFX"),
        ("nonassoc", "ELSE"),
        ("nonassoc", "LE", "GE", "LT", "GT", "EQ", "NEQ"),
        ("left", "+", "-", "DOTPLUS", "DOTMINUS"),
        ("left", "*", "/", "DOTTIMES", "DOTDIVIDE"),
        ("right", "UMINUS", "\'"),
    )

    @_("block start", "block")
    def start(self, p):
        if hasattr(p, 'block') and hasattr(p, 'start'):
            return AST.Block(p.block + p.start.statements)
        return AST.Block(p.block)

    @_("ID")
    def expression(self, p):
        return AST.Variable(p.ID)

    @_("STRING")
    def expression(self, p):
        return AST.String(p.STRING)

    @_("INTNUM")
    def expression(self, p):
        return AST.IntNum(int(p.INTNUM))

    @_("FLOATNUM")
    def expression(self, p):
        return AST.FloatNum(float(p.FLOATNUM))

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
        return AST.BinExpr(p[1], p.expression0, p.expression1)

    @_("expression LT expression", "expression GT expression",
       "expression LE expression", "expression GE expression",
       "expression NEQ expression", "expression EQ expression")
    def expression(self, p):
        return AST.BinExpr(p[1], p.expression0, p.expression1)

    @_("expression '\''")
    def expression(self, p):
        return AST.Transpose(p.expression)

    @_("'-' expression %prec UMINUS")
    def expression(self, p):
        return AST.BinExpr("-", AST.IntNum(0), p.expression)

    @_("ZEROS '(' expression ')' ")
    def expression(self, p):
        return AST.Zeros(p.expression)

    @_("ONES '(' expression ')' ")
    def expression(self, p):
        return AST.Ones(p.expression)

    @_("EYE '(' expression ')'")
    def expression(self, p):
        return AST.Eye(p.expression)

    @_("'[' list ']'")
    def expression(self, p):
        return AST.Array(p.list)

    @_("spread_elements ',' list_element", "list_element")
    def spread_elements(self, p):
        if len(p) == 3:
            return AST.Array(p.spread_elements, [p.list_element])
        else:
            return AST.Array([p.list_element])

    @_("list ',' '[' spread_elements ']'", "'[' spread_elements ']'")
    def list(self, p):
        return AST.Array([p.spread_elements])

    @_("INTNUM", "FLOATNUM", "STRING", "ID")
    def list_element(self, p):
        if isinstance(p[0], int):
            return AST.IntNum(p[0])
        elif isinstance(p[0], float):
            return AST.FloatNum(p[0])
        elif p[0][0] in ('"', "'"):  # Check for string literals
            return AST.String(p[0])
        else:
            return AST.Variable(p[0])

    @_("IF '(' expression ')' block ELSE block")
    def statement(self, p):
        return AST.IfElse(p.expression, AST.Block(p.block0), AST.Block(p.block1))

    @_("IF '(' expression ')' block %prec IFX")
    def statement(self, p):
        return AST.IfElse(p.expression, AST.Block(p.block))

    @_("WHILE '(' expression ')' block")
    def statement(self, p):
        return AST.WhileLoop(p.expression, AST.Block(p.block))

    @_("FOR ID '=' range block")
    def statement(self, p):
        return AST.ForLoop(AST.Variable(p.ID), p.range, AST.Block(p.block))

    @_("assignable '=' expression ';'",
       "assignable ADDASSIGN expression ';'",
       "assignable SUBASSIGN expression ';'",
       "assignable MULASSIGN expression ';'",
       "assignable DIVASSIGN expression ';'")
    def statement(self, p):
        return AST.Assignment(p.assignable, p[1], p.expression)

    @_("RETURN expression ';'")
    def statement(self, p):
        return AST.Return(p.expression)

    @_("CONTINUE ';'")
    def statement(self, _):
        return AST.Continue()

    @_("BREAK ';'")
    def statement(self, _):
        return AST.Break()

    @_("expression ';'")
    def statement(self, p):
        if isinstance(p.expression, (AST.Zeros, AST.Ones, AST.Eye)):
            return p.expression

    @_("PRINT prints ';'")
    def statement(self, p):
        return AST.Print(p.prints)

    @_("statement", "'{' spread_statements '}'")
    def block(self, p):
        if len(p) == 1:
            return [p.statement]
        return p.spread_statements

    @_("statement spread_statements", "statement")
    def spread_statements(self, p):
        if len(p) == 2:
            return [p.statement] + p.spread_statements
        return [p.statement]

    @_("expression ',' prints", "expression")
    def prints(self, p):
        if len(p) == 3:
            return [p.expression] + p.prints
        else:
            return [p.expression]

    @_("INTNUM ':' INTNUM", "ID ':' ID", "ID ':' INTNUM", "INTNUM ':' ID")
    def range(self, p):
        tmp1 = AST.IntNum(p[0]) if isinstance(p[0], int) else AST.Variable(p[0])
        tmp2 = AST.IntNum(p[2]) if isinstance(p[2], int) else AST.Variable(p[2])
        return AST.ArrayRange(tmp1, tmp2)

    @_("ID", "ID '[' indexes ']'")
    def assignable(self, p):
        if len(p) == 1:
            return AST.Variable(p[0])
        else:
            return AST.ArrayAccess(p[0], p.indexes)

    @_("INTNUM ',' indexes", "INTNUM")
    def indexes(self, p):
        if len(p) == 1:
            return [AST.IntNum(p[0])]
        else:
            return [AST.IntNum(p[0])] + p.indexes
