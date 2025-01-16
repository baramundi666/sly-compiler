import src.AST as AST
from src.memory import *
from src.exceptions import *
from src.operation_map import OperationMap
from src.visitor import *
from src.type_checker import *
import sys


sys.setrecursionlimit(10000)


class Interpreter(object):
    def __init__(self):
        self.memory_stack = MemoryStack(Memory("global"))
        self.memory_stack.insert("_FOR_", 0)
        self.memory_stack.insert("_WHILE_", 0)
        self.operation_map = OperationMap().operation_map
        self.type_table = TypeTable()

    @on("node")
    def visit(self, node):
        pass

    @when(AST.IntNum)
    def visit(self, node):
        return ScalarType("intnum", node.value)

    @when(AST.FloatNum)
    def visit(self, node):
        return ScalarType("floatnum", node.value)

    @when(AST.String)
    def visit(self, node):
        return ScalarType("string", node.value)

    @when(AST.Variable)
    def visit(self, node):
        variable_value = self.memory_stack.get(node.name)
        if variable_value is None:
            return UndefinedType()
        return variable_value

    @when(AST.BinExpr)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if isinstance(left, MatrixType):
            return self.operation_map[node.op](left, right)
        return ScalarType(
            self.type_table.getType(left.typeOfValue, node.op, right.typeOfValue),
            self.operation_map[node.op](left.content, right.content),
        )

    @when(AST.Transpose)
    def visit(self, node):
        val = self.visit(node.expression)
        return self.operation_map["'"](val)

    @when(AST.Zeros)
    def visit(self, node):
        n, m = node.sizes if len(node.sizes) == 2 else (node.sizes[0], node.sizes[0])
        n, m = self.visit(n).content, self.visit(m).content
        zeros_matrix = [[ScalarType("intnum", 0) for j in range(m)] for i in range(n)]
        return MatrixType("intnum", n, m, zeros_matrix)

    @when(AST.Ones)
    def visit(self, node):
        n, m = node.sizes if len(node.sizes) == 2 else (node.sizes[0], node.sizes[0])
        n, m = self.visit(n).content, self.visit(m).content
        ones_matrix = [[ScalarType("intnum", 1) for j in range(m)] for i in range(n)]
        return MatrixType("intnum", n, m, ones_matrix)

    @when(AST.Eye)
    def visit(self, node):
        n, m = node.sizes if len(node.sizes) == 2 else (node.sizes[0], node.sizes[0])
        n, m = self.visit(n).content, self.visit(m).content
        eye_matrix = [[ScalarType("intnum", 1) if i == j else ScalarType("intnum", 0) for j in range(m)] for i in range(n)]
        return MatrixType("intnum", n, m, eye_matrix)

    @when(AST.Block)
    def visit(self, node):
        self.visit(node.statement)
        if node.next_statements is not None:
            self.visit(node.next_statements)
        return SuccessType()

    @when(AST.Statement)
    def visit(self, node):
        self.visit(node.statement)
        if node.next_statements is not None:
            self.visit(node.next_statements)
        return SuccessType()

    @when(AST.Continue)
    def visit(self, node):
        raise ContinueException()

    @when(AST.Break)
    def visit(self, node):
        raise BreakException()

    @when(AST.Return)
    def visit(self, node):
        raise ReturnValueException(self.visit(node.expression))

    @when(AST.Assignment)
    def visit(self, node):
        action = node.op.replace("=", "")
        left = self.visit(node.variable)
        right = self.visit(node.value)
        variable_value = ScalarType(
            self.type_table.getType(left.typeOfValue, node.op, right.typeOfValue),
            self.operation_map[action](left.content, right.content),
        ) if action else right

        if isinstance(node.variable, AST.Variable):
            variable_name = node.variable.name
            self.memory_stack.insert(variable_name, variable_value)
        elif isinstance(node.variable, AST.ArrayAccess):
            variable_name = node.variable.array.name
            array = self.memory_stack.get(variable_name)
            variable_value = self.visit(node.value)
            array.content[node.variable.indexes[0].value][
                node.variable.indexes[0].value
            ] = variable_value
            self.memory_stack.set(variable_name, array)

    @when(AST.ArrayRange)
    def visit(self, node):
        start = self.visit(node.start)
        end = self.visit(node.end)
        return RangeType(start=start, end=end)

    @when(AST.ForLoop)
    def visit(self, node):
        variable_name = node.variable.name
        range_ = self.visit(node.range)
        self.memory_stack.set("_FOR_", self.memory_stack.get("_FOR_") + 1)
        try:
            for i in range(range_.start.content, range_.end.content + 1):
                self.memory_stack.insert(variable_name, ScalarType("intnum", i))
                try:
                    self.visit(node.block)
                except ContinueException:
                    pass
        except BreakException:
            pass
        self.memory_stack.set(variable_name, None)
        self.memory_stack.set("_FOR_", self.memory_stack.get("_FOR_") - 1)
        return SuccessType()

    @when(AST.WhileLoop)
    def visit(self, node):
        self.memory_stack.set("_WHILE_", self.memory_stack.get("_WHILE_") + 1)
        try:
            while self.visit(node.condition).content:
                try:
                    self.visit(node.block)
                except ContinueException:
                    pass
        except BreakException:
            pass
        self.memory_stack.set("_WHILE_", self.memory_stack.get("_WHILE_") - 1)
        return SuccessType()

    @when(AST.IfElse)
    def visit(self, node):
        condition = self.visit(node.condition)
        if condition.content:
            self.visit(node.if_block)
        elif node.else_block is not None:
            self.visit(node.else_block)
        return SuccessType()

    @when(AST.ArrayAccess)
    def visit(self, node):
        array = self.visit(node.array)
        viewed = array.content[self.visit(node.indexes[0]).content][
            self.visit(node.indexes[1]).content
        ].content
        return ScalarType(array.typeOfValue, viewed)

    @when(AST.Array)
    def visit(self, node):
        elements = self.visit(node.elements)
        if isinstance(elements.content[0], list):
            return elements
        val = [ScalarType("floatnum", float(el.content)) for el in elements.content]


        typeOfContent = val[0].typeOfValue
        if node.other is not None:
            other = self.visit(node.other)
            return MatrixType(
                typeOfValue=typeOfContent,
                rows=1 + other.rows(),
                columns=other.columns(),
                value=[val] + other.content,
            )

        return MatrixType(
            typeOfValue=typeOfContent, rows=1, columns=len(val), value=[val]
        )

    @when(AST.Spread)
    def visit(self, node):
        elements = [self.visit(node.element)]
        if node.next is not None:
            next_item = self.visit(node.next)
            elements.extend(next_item.content)

        return SpreadType(elements)

    @when(AST.Print)
    def visit(self, node):
        elements = self.visit(node.expressions)
        print("stdout:", end=" ")
        n = len(elements.content)
        for i, element in enumerate(elements.content):
            if isinstance(element, MatrixType):
                print("[", end="")
                for j, row in enumerate(element.content):
                    print("[", end="")
                    for k, scalar in enumerate(row):
                        print(scalar.content, end="")
                        if k != len(row) - 1:
                            print(", ", end="")
                    print("]", end="")
                    if j != len(element.content) - 1:
                        print(", ", end="")
                print("]", end="")
            else:
                print(element.content, end="")
            if i != n - 1:
                print(", ", end="")

        print()
        return SuccessType()
