class Node(object):
    pass


class IntNum(Node):
    def __init__(self, value):
        self.value = value


class FloatNum(Node):
    def __init__(self, value):
        self.value = value


class String(Node):
    def __init__(self, value):
        self.value = value


class Variable(Node):
    def __init__(self, name):
        self.name = name


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class Transpose(Node):
    def __init__(self, expression):
        self.expression = expression


class Zeros(Node):
    def __init__(self, size):
        self.size = size


class Ones(Node):
    def __init__(self, size):
        self.size = size


class Eye(Node):
    def __init__(self, size):
        self.size = size


class Array(Node):
    def __init__(self, elements, other=None):
        self.elements = elements
        self.other = other

class Spread(Node):
    def __init__(self, element, next=None):
        self.element = element
        self.next = next

class ArrayAccess(Node):
    def __init__(self, array, indexes):
        self.array = array
        self.indexes = indexes


class IfElse(Node):
    def __init__(self, condition, if_block, else_block=None):
        self.condition = condition
        self.if_block = if_block
        self.else_block = else_block


class WhileLoop(Node):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block


class ForLoop(Node):
    def __init__(self, variable, range_, block):
        self.variable = variable
        self.range = range_
        self.block = block


class Assignment(Node):
    def __init__(self, variable, op, value):
        self.variable = variable
        self.op = op
        self.value = value


class Return(Node):
    def __init__(self, expression):
        self.expression = expression


class Continue(Node):
    pass


class Break(Node):
    pass


class Print(Node):
    def __init__(self, expressions):
        self.expressions = expressions


class Block(Node):
    def __init__(self, statement, next_statements=None):
        self.statement = statement
        self.next_statements = next_statements


class Statement(Node):
    def __init__(self, statement, next_statements=None):
        self.statement = statement
        self.next_statements = next_statements


class ArrayRange(Node):
    def __init__(self, start, end):
        self.start = start
        self.end = end