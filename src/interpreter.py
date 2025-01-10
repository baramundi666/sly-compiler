import src.AST as AST
from src.symbol_table import TypeTable
from src.memory import *
from src.exceptions import *
from src.operation_map import OperationMap
from src.types import *
from src.visitor import *
import sys


sys.setrecursionlimit(10000)


class Interpreter(object):
    def __init__(self):
        self.memory_stack = MemoryStack(Memory("global"))
        self.operation_map = OperationMap().operation_map
        self.type_table = TypeTable()

    @on("node")
    def visit(self, node):
        pass

    @when(AST.IntNum)
    def visit(self, node):
        # print("visit AST.IntNum")
        return ScalarType("intnum", node.value)

    @when(AST.FloatNum)
    def visit(self, node):
        # print("visit AST.FloatNum")
        return ScalarType("floatnum", node.value)

    @when(AST.String)
    def visit(self, node):
        # print("visit AST.String")
        return ScalarType("string", node.value)

    @when(AST.Variable)
    def visit(self, node):
        # print("visit AST.Variable")
        variable_value = self.memory_stack.get(node.name)
        if variable_value is None:
            return UndefinedType()
        return variable_value

    @when(AST.BinExpr)
    def visit(self, node):
        # print("visit AST.BinExpr")
        left = self.visit(node.left)
        right = self.visit(node.right)
        if left.shapeOfValue != right.shapeOfValue:
            raise RuntimeException(
                f"Line {node.lineno}: incorrect shapes {left.shapeOfValue} and {right.shapeOfValue}"
            )
        return ScalarType(
            self.type_table.getType(left.typeOfValue, node.op, right.typeOfValue),
            self.operation_map[node.op](left.content, right.content),
        )

    @when(AST.Transpose)
    def visit(self, node):
        # print("visit AST.Transpose")
        return self.operation_map["'"](self.visit(node.expression))

    @when(AST.Zeros)
    def visit(self, node):
        # print("visit AST.Zeros")
        n, m = node.sizes if len(node.sizes) == 2 else (node.sizes[0], node.sizes[0])
        n, m = self.visit(n).content, self.visit(m).content
        zeros_matrix = [[0 for j in range(m)] for i in range(n)]
        return MatrixType("intnum", n, m, zeros_matrix)

    @when(AST.Ones)
    def visit(self, node):
        # print("visit AST.Ones")
        n, m = node.sizes if len(node.sizes) == 2 else (node.sizes[0], node.sizes[0])
        n, m = self.visit(n).content, self.visit(m).content
        ones_matrix = [[1 for j in range(m)] for i in range(n)]
        return MatrixType("intnum", n, m, ones_matrix)

    @when(AST.Eye)
    def visit(self, node):
        # print("visit AST.Eye")
        n, m = node.sizes if len(node.sizes) == 2 else (node.sizes[0], node.sizes[0])
        n, m = self.visit(n).content, self.visit(m).content
        eye_matrix = [[1 if i == j else 0 for j in range(m)] for i in range(n)]
        return MatrixType("intnum", n, m, eye_matrix)

    @when(AST.Block)
    def visit(self, node):
        # print("visit AST.Block")
        self.visit(node.statement)
        if node.next_statements is not None:
            self.visit(node.next_statements)
        return SuccessType()

    @when(AST.Statement)
    def visit(self, node):
        # print("visit AST.Statement")
        self.visit(node.statement)
        if node.next_statements is not None:
            self.visit(node.next_statements)
        return SuccessType()

    @when(AST.Continue)
    def visit(self, node):
        # print("visit AST.Continue")
        if not self.memory_stack.top_memory.has_key(
            "_FOR_"
        ) and not self.memory_stack.top_memory.has_key("_WHILE_"):
            raise RuntimeException(
                f"Line {node.lineno}: continue statement outside of loop"
            )
        raise ContinueException()

    @when(AST.Break)
    def visit(self, node):
        # print("visit AST.Break")
        if not self.memory_stack.top_memory.has_key(
            "_FOR_"
        ) and not self.memory_stack.top_memory.has_key("_WHILE_"):
            raise RuntimeException(
                f"Line {node.lineno}: break statement outside of loop"
            )
        raise BreakException()

    @when(AST.Return)
    def visit(self, node):
        # print("visit AST.Return")
        raise ReturnValueException(self.visit(node.expression))

    @when(AST.Assignment)
    def visit(self, node):
        # print("visit AST.Assignment")
        if isinstance(node.variable, AST.Variable):
            variable_name = node.variable.name
            variable_value = self.visit(node.value)
            self.memory_stack.insert(variable_name, variable_value)
        elif isinstance(node.variable, AST.ArrayAccess):
            variable_name = node.variable.array.name
            array = self.memory_stack.get(variable_name)

            viewed = self.visit(
                node.variable
            )  # ignored here, but used for printing accessed value
            variable_value = self.visit(node.value)
            # array = self.visit(node.variable).full_array
            array.content[node.variable.indexes[0].value][
                node.variable.indexes[0].value
            ] = variable_value.content
            self.memory_stack.set(variable_name, array)

    @when(AST.ArrayRange)
    def visit(self, node):
        # print("visit AST.ArrayRange")
        start = self.visit(node.start)
        end = self.visit(node.end)
        return RangeType(start=start, end=end)

    @when(AST.ForLoop)
    def visit(self, node):
        # print("visit AST.ForLoop")
        variable_name = node.variable.name
        range_ = self.visit(node.range)
        self.memory_stack.insert("_FOR_", True)
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
        self.memory_stack.set("_FOR_", None)
        return SuccessType()

    @when(AST.WhileLoop)
    def visit(self, node):
        # print("visit AST.WhileLoop")
        self.memory_stack.insert("_WHILE_", True)
        try:
            while self.visit(node.condition):
                try:
                    self.visit(node.block)
                except ContinueException:
                    pass
        except BreakException:
            pass
        self.memory_stack.set("_WHILE_", None)
        return SuccessType()

    @when(AST.IfElse)
    def visit(self, node):
        # print("visit AST.IfElse")
        condition = self.visit(node.condition)
        if condition.value:
            self.visit(node.block)
        elif node.else_block is not None:
            self.visit(node.else_block)
        return SuccessType()

    @when(AST.ArrayAccess)
    def visit(self, node):
        # print("visit AST.ArrayAccess")
        array = self.visit(node.array)
        viewed = array.content[self.visit(node.indexes[0]).content][
            self.visit(node.indexes[1]).content
        ]
        if isinstance(viewed, float):
            return ScalarType("floatnum", viewed)
        return ScalarType("intnum", viewed)

    @when(AST.Array)
    def visit(self, node):
        # print("visit AST.Array")
        # TODO
        elements = self.visit(node.elements)
        if node.other is not None:
            other = self.visit(node.other)
            elements += other
        return MatrixType("intnum", len(elements), 1, elements)

    @when(AST.Spread)
    def visit(self, node):
        # print("visit AST.Spread")
        elements = [self.visit(node.element)]
        next_ = node.next
        next_item = self.visit(next_)
        if next_item:
            elements += next_item.content
        return SpreadType(elements)

    @when(AST.Print)
    def visit(self, node):
        # print("visit AST.Print")
        elements = self.visit(node.expressions)
        print("stdout:", end=" ")
        n = len(elements.content)
        for i, element in enumerate(elements.content):
            print(element.content, end="")
            if i != n - 1:
                print(", ", end="")

        print()
        return SuccessType()
