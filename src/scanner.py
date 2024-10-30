import sly


Lexer = sly.Lexer


class MyToken(sly.lex.Token):
    def __repr__(self):
        return f"({self.lineno}): {self.type}({self.value})"


sly.lex.Token = MyToken


class Scanner(Lexer):
    tokens = [
        "DOTPLUS",
        "DOTMINUS",
        "DOTTIMES",
        "DOTDIVIDE",
        "ADDASSIGN",
        "SUBASSIGN",
        "MULASSIGN",
        "DIVASSIGN",
        "EQ",
        "NEQ",
        "LE",
        "GE",
        "LT",
        "GT",
        "ID",
        "IF",
        "ELSE",
        "FOR",
        "WHILE",
        "BREAK",
        "CONTINUE",
        "RETURN",
        "EYE",
        "ZEROS",
        "ONES",
        "PRINT",
        "FLOATNUM",
        "INTNUM",
        "STRING",
        "SKIP",
        "COMMENT",
    ]

    literals = {
        "+",
        "-",
        "*",
        "/",
        "(",
        ")",
        "[",
        "]",
        "{",
        "}",
        ":",
        "'",
        ",",
        ";",
        "=",
    }

    # Regular expression rules for tokens
    DOTPLUS = r"\.\+"
    DOTMINUS = r"\.\-"
    DOTTIMES = r"\.\*"
    DOTDIVIDE = r"\.\/"

    ADDASSIGN = r"\+="
    SUBASSIGN = r"\-="
    MULASSIGN = r"\*="
    DIVASSIGN = r"\/="

    EQ = r"=="
    NEQ = r"!="
    LE = r"<="
    GE = r">="
    LT = r"<"
    GT = r">"

    # Identifiers and keywords
    ID = r"[a-zA-Z_][a-zA-Z0-9_]*"
    ID["if"] = "IF"
    ID["else"] = "ELSE"
    ID["for"] = "FOR"
    ID["while"] = "WHILE"
    ID["break"] = "BREAK"
    ID["continue"] = "CONTINUE"
    ID["return"] = "RETURN"
    ID["eye"] = "EYE"
    ID["zeros"] = "ZEROS"
    ID["ones"] = "ONES"
    ID["print"] = "PRINT"

    FLOATNUM = r"([0-9]+\.([0-9]+)?|\.[0-9]+)([eE][+-]?[0-9]+)?"
    INTNUM = r"\d+"
    STRING = r"\".*?\"|\'.*?\'"

    ignore = ' \t'
    ignore_comment = r'\#.*'

    @_(r"\n")
    def NEWLINE(self, _):
        self.lineno += 1

    def error(self, t):
        print(f"Line {self.lineno}: Bad character \"{t.value[0]}\"")
