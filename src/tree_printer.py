import src.AST as AST


def addToClass(cls):
    def decorator(func):
        setattr(cls, func.__name__, func)
        return func

    return decorator


def print_indent(indent, text):
    print("| " * indent, text, sep="")


class TreePrinter:
    @addToClass(AST.Node)
    def printTree(self, indent=0):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.IntNum)
    def printTree(self, indent=0):
        print_indent(indent, str(self.value))

    @addToClass(AST.FloatNum)
    def printTree(self, indent=0):
        print_indent(indent, str(self.value))

    @addToClass(AST.String)
    def printTree(self, indent=0):
        print_indent(indent, self.value)

    @addToClass(AST.Variable)
    def printTree(self, indent=0):
        print_indent(indent, self.name)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        print_indent(indent, self.op)
        self.left.printTree(indent + 1)
        self.right.printTree(indent + 1)

    @addToClass(AST.Transpose)
    def printTree(self, indent=0):
        print_indent(indent, "TRANSPOSE")
        self.expression.printTree(indent + 1)

    @addToClass(AST.Zeros)
    def printTree(self, indent=0):
        print_indent(indent, "ZEROS")
        for index in self.sizes:
            index.printTree(indent + 1)

    @addToClass(AST.Ones)
    def printTree(self, indent=0):
        print_indent(indent, "ONES")
        for index in self.sizes:
            index.printTree(indent + 1)

    @addToClass(AST.Eye)
    def printTree(self, indent=0):
        print_indent(indent, "EYE")
        for index in self.sizes:
            index.printTree(indent + 1)

    @addToClass(AST.Array)
    def printTree(self, indent=0):
        print_indent(indent, "VECTOR")
        self.elements.printTree(indent + 1)
        if self.other is not None:
            self.other.printTree(indent)

    @addToClass(AST.Spread)
    def printTree(self, indent=0):
        self.element.printTree(indent)
        if self.next is not None:
            self.next.printTree(indent)

    @addToClass(AST.ArrayAccess)
    def printTree(self, indent=0):
        print_indent(indent, "REF")
        self.array.printTree(indent + 1)
        for index in self.indexes:
            index.printTree(indent + 1)

    @addToClass(AST.IfElse)
    def printTree(self, indent=0):
        print_indent(indent, "IF")
        self.condition.printTree(indent + 1)
        print_indent(indent + 1, "THEN")
        self.if_block.printTree(indent + 2)
        if self.else_block:
            print_indent(indent + 1, "ELSE")
            self.else_block.printTree(indent + 2)

    @addToClass(AST.WhileLoop)
    def printTree(self, indent=0):
        print_indent(indent, "WHILE")
        self.condition.printTree(indent + 1)
        self.block.printTree(indent + 1)

    @addToClass(AST.ForLoop)
    def printTree(self, indent=0):
        print_indent(indent, "FOR")
        self.variable.printTree(indent + 1)
        self.range.printTree(indent + 1)
        self.block.printTree(indent + 1)

    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        print_indent(indent, self.op)
        self.variable.printTree(indent + 1)
        self.value.printTree(indent + 1)

    @addToClass(AST.Return)
    def printTree(self, indent=0):
        print_indent(indent, "RETURN")
        self.expression.printTree(indent + 1)

    @addToClass(AST.Continue)
    def printTree(self, indent=0):
        print_indent(indent, "CONTINUE")

    @addToClass(AST.Break)
    def printTree(self, indent=0):
        print_indent(indent, "BREAK")

    @addToClass(AST.Print)
    def printTree(self, indent=0):
        print_indent(indent, "PRINT")
        self.expressions.printTree(indent + 1)

    @addToClass(AST.Block)
    def printTree(self, indent=0):
        self.statement.printTree(indent)
        if self.next_statements is not None:
            self.next_statements.printTree(indent)

    @addToClass(AST.Statement)
    def printTree(self, indent=0):
        self.statement.printTree(indent)
        if self.next_statements is not None:
            self.next_statements.printTree(indent)

    @addToClass(AST.ArrayRange)
    def printTree(self, indent=0):
        print_indent(indent, "RANGE")
        self.start.printTree(indent + 1)
        self.end.printTree(indent + 1)
