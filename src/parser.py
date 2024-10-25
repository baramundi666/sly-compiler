from sly import Parser
from scanner import Scanner


class Mparser(Parser):
    tokens = Scanner.tokens

    debugfile = "parser.out"

    precedence = (
        ("nonassoc", "ADDASSIGN",
        "SUBASSIGN",
        "MULASSIGN",
        "DIVASSIGN"),
        ("nonassoc", "LE", "GE", "LT", "GT", "EQ", "NEQ"),
        ("left", "+", "-"),
        ("left", "*", "/"),
        ("left", "DOTPLUS", "DOTMINUS"),
        ("left", "DOTTIMES", "DOTDIVIDE"),

    )

    @_("instructions_opt")
    def p_program(p):
        pass

    @_("instructions")
    def p_instructions_opt(p):
        pass

    @_("")
    def p_instructions_opt(p):
        pass

    @_("instructions instruction")
    def p_instructions(p):
        pass

    @_("instruction")
    def p_instructions(p):
        pass

    # to finish the grammar
    # ....
