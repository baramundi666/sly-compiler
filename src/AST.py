class Node(object):
    def __init__(self, lineno):
        self.lineno = lineno

    def visit(self, visitor):
        try:
            func = getattr(visitor, f"visit_{self.__class__.__name__}")
            return func(self)
        except AttributeError:
            print(
                f"Visitor {visitor.__class__.__name__} does not have visit_{self.__class__.__name__} implemented"
            )


class IntNum(Node):
    def __init__(self, value, typeOfValue="intnum", lineno=0):
        super().__init__(lineno)
        self.typeOfValue = typeOfValue
        self.value = value


class FloatNum(Node):
    def __init__(self, value, typeOfValue="floatnum", lineno=0):
        super().__init__(lineno)
        self.typeOfValue = typeOfValue
        self.value = value


class String(Node):
    def __init__(self, value, typeOfValue="string", lineno=0):
        super().__init__(lineno)
        self.typeOfValue = typeOfValue
        self.value = value


class Variable(Node):
    def __init__(self, name, lineno=0):
        super().__init__(lineno)
        self.name = name


class BinExpr(Node):
    def __init__(self, op, left, right, lineno=0):
        super().__init__(lineno)
        self.op = op
        self.left = left
        self.right = right


class Transpose(Node):
    def __init__(self, expression, lineno=0):
        super().__init__(lineno)
        self.expression = expression


class Zeros(Node):
    def __init__(self, sizes, lineno=0):
        super().__init__(lineno)
        self.sizes = sizes


class Ones(Node):
    def __init__(self, sizes, lineno=0):
        super().__init__(lineno)
        self.sizes = sizes


class Eye(Node):
    def __init__(self, sizes, lineno=0):
        super().__init__(lineno)
        self.sizes = sizes


class Array(Node):
    def __init__(self, elements, other=None, lineno=0):
        super().__init__(lineno)
        self.elements = elements
        self.other = other


class Spread(Node):
    def __init__(self, element, next=None, lineno=0):
        super().__init__(lineno)
        self.element = element
        self.next = next


class ArrayAccess(Node):
    def __init__(self, array, indexes, lineno=0):
        super().__init__(lineno)
        self.array = array
        self.indexes = indexes


class IfElse(Node):
    def __init__(self, condition, if_block, else_block=None, lineno=0):
        super().__init__(lineno)
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block


class WhileLoop(Node):
    def __init__(self, condition, block, lineno=0):
        super().__init__(lineno)
        self.condition = condition
        self.block = block


class ForLoop(Node):
    def __init__(self, variable, range_, block, lineno=0):
        super().__init__(lineno)
        self.variable = variable
        self.range = range_
        self.block = block


class Assignment(Node):
    def __init__(self, variable, op, value, lineno=0):
        super().__init__(lineno)
        self.variable = variable
        self.op = op
        self.value = value


class Return(Node):
    def __init__(self, expression, lineno=0):
        super().__init__(lineno)
        self.expression = expression


class Continue(Node):
    pass


class Break(Node):
    pass


class Print(Node):
    def __init__(self, expressions, lineno=0):
        super().__init__(lineno)
        self.expressions = expressions


class Block(Node):
    def __init__(self, statement, next_statements=None, lineno=0):
        super().__init__(lineno)
        self.statement = statement
        self.next_statements = next_statements


class Statement(Node):
    def __init__(self, statement, next_statements=None, lineno=0):
        super().__init__(lineno)
        self.statement = statement
        self.next_statements = next_statements


class ArrayRange(Node):
    def __init__(self, start, end, lineno=0):
        super().__init__(lineno)
        self.start = start
        self.end = end
