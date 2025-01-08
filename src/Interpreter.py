
import AST
import SymbolTable
from Memory import *
from Exceptions import  *
from src.OperationMap import OperationMap
from src.TypeChecker import ScalarType, UndefinedType, MatrixType, SuccessType, RangeType, SpreadType
from visit import *
import sys

sys.setrecursionlimit(10000)

class Interpreter(object):
    def __init__(self):
        self.global_memory = MemoryStack(Memory("global"))
        self.operation_map = OperationMap.operation_map

    @on('node')
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
        variable_value = self.global_memory.top_memory.get(node.name)
        if variable_value is None:
            return UndefinedType()
        return variable_value

    @when(AST.BinExpr)
    def visit(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        if left.shapeOfValue != right.shapeOfValue:
            raise RuntimeException(f"Line {node.lineno}: incorrect shapes {left.shapeOfValue} and {right.shapeOfValue}")
        return self.operation_map[node.op](left, right)

    @when(AST.Transpose)
    def visit(self, node):
        return self.operation_map["'"](self.visit(node.expression))

    @when(AST.Zeros)
    def visit(self, node):
        n, m = node.sizes
        zeros_matrix = [[0 for _ in range(m)] for _ in range(n)]
        return MatrixType("intnum", n, m, zeros_matrix)

    @when(AST.Ones)
    def visit(self, node):
        n, m = node.sizes
        ones_matrix = [[1 for _ in range(m)] for _ in range(n)]
        return MatrixType("intnum", n, m, ones_matrix)

    @when(AST.Eye)
    def visit(self, node):
        n, m = node.sizes
        eye_matrix = [[1 if i == j else 0 for j in range(m)] for i in range(n)]
        return MatrixType("intnum", n, m, eye_matrix)

    @when(AST.Block)
    def visit(self, node):
        self.global_memory.push(Memory("block"))
        self.visit(node.statement)
        if node.next_statements is not None:
            self.visit(node.next_statements)
        self.global_memory.pop()
        return SuccessType()

    @when(AST.Statement)
    def visit(self, node):
        self.global_memory.push(Memory("statement"))
        self.visit(node.statement)
        if node.next_statements is not None:
            self.visit(node.next_statements)
        self.global_memory.pop()
        return SuccessType()

    @when(AST.Continue)
    def visit(self, node):
        top_memory_name = self.global_memory.top_memory.name
        if top_memory_name not in ("for", "while"):
            raise RuntimeException(f"Line {node.lineno}: continue statement outside of loop")
        raise ContinueException()

    @when(AST.Break)
    def visit(self, node):
        top_memory_name = self.global_memory.top_memory.name
        if top_memory_name not in ("for", "while"):
            raise RuntimeException(f"Line {node.lineno}: break statement outside of loop")
        raise BreakException()

    @when(AST.Return)
    def visit(self, node):
        raise ReturnValueException(self.visit(node.expression))

    @when(AST.Assignment)
    def visit(self, node):
        variable_name = node.variable.name
        variable_value = self.visit(node.value)
        self.global_memory.top_memory.put(variable_name, variable_value)
        return variable_value

    @when(AST.ArrayRange)
    def visit(self, node):
        start = self.visit(node.start)
        end = self.visit(node.end)
        return RangeType(start=start, end=end)

    @when(AST.ForLoop)
    def visit(self, node):
        self.global_memory.push(Memory("for"))
        variable_name = node.variable.name
        range_ = self.visit(node.range)
        try:
            for i in range(range_.start.value, range_.end.value + 1):
                self.global_memory.top_memory.put(variable_name, ScalarType("intnum", i))
                try:
                    self.visit(node.block)
                except ContinueException:
                    pass
        except BreakException:
            pass
        self.global_memory.pop()
        return SuccessType()

    @when(AST.WhileLoop)
    def visit(self, node):
        self.global_memory.push(Memory("while"))
        try:
            while self.visit(node.condition):
                try:
                    self.visit(node.block)
                except ContinueException:
                    pass
        except BreakException:
            pass
        self.global_memory.pop()
        return SuccessType()

    @when(AST.IfElse)
    def visit(self, node):
        condition = self.visit(node.condition)
        if condition.value:
            self.visit(node.block)
        elif node.else_block is not None:
            self.visit(node.else_block)
        return SuccessType()

    @when(AST.ArrayAccess)
    def visit(self, node):
        array = self.visit(node.array)
        indexes = [self.visit(index) for index in node.indexes]
        if array.typeOfValue == "matrix":
            return array.value[indexes[0]][indexes[1]]
        else:
            return array.value[indexes[0]]

    @when(AST.Array)
    def visit(self, node):
        elements = self.visit(node.elements)
        if node.other is not None:
            other = self.visit(node.other)
            elements += other
        return elements

    @when(AST.Spread)
    def visit(self, node):
        elements = self.visit(node.element)
        if node.next is not None:
            next_ = self.visit(node.next)
            elements += next_
        return SpreadType(elements)

    @when(AST.Print)
    def visit(self, node):
        elements = self.visit(node.expressions)
        print(elements)
        return SuccessType()

