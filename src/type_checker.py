from src.AST import (
    BinExpr,
    String,
    FloatNum,
    IntNum,
    Transpose,
    Zeros,
    Array,
    Block,
    Statement,
    Continue,
    Break,
    Return,
    Assignment,
    Variable,
    ArrayRange,
    ForLoop,
    WhileLoop,
    IfElse,
    ArrayAccess,
    Spread,
    Print,
)
from src.symbol_table import SymbolTable, TypeTable


class BaseType(object):
    def __init__(
        self, entityType, typeOfValue=None, shapeOfValue=None, content=None, name=None
    ):
        self.entityType = entityType
        self.typeOfValue = typeOfValue
        self.shapeOfValue = shapeOfValue
        self.content = content
        self.name = name


class ScalarType(BaseType):
    def __init__(self, typeOfValue, value, name=None):
        super().__init__(
            "scalar", typeOfValue=typeOfValue, shapeOfValue=(), content=value, name=name
        )

    @staticmethod
    def columns(self):
        return 1


class ErrorType(BaseType):
    def __init__(self, reason):
        super().__init__(entityType="error", content=reason)
        print(reason)


class SuccessType(BaseType):
    def __init__(self):
        super().__init__(entityType="success")


class UndefinedType(BaseType):
    def __init__(self):
        super().__init__(entityType="undefined")


class VectorType(BaseType):
    def __init__(self, typeOfValue, length, value):
        super().__init__(
            entityType="vector",
            typeOfValue=typeOfValue,
            shapeOfValue=(length,),
            content=value,
        )

    def rows(self):
        return 1

    def columns(self):
        return self.shapeOfValue[0]

    def valueAt(self, index):
        if self.content is None or index is None:
            return None
        return self.content[index]


class MatrixType(BaseType):
    def __init__(self, typeOfValue, rows, columns, value, name=None):
        super().__init__(
            "matrix",
            typeOfValue=typeOfValue,
            shapeOfValue=(rows, columns),
            content=value,
            name=name,
        )

    def rows(self):
        return self.shapeOfValue[0]

    def columns(self):
        return self.shapeOfValue[1]

    def valueAt(self, row, column=None):
        if self.content is None or row is None:
            return None
        if column is None:
            return self.content[row]
        if row == ":":
            values = ()
            for vector in self.content:
                values = (*values, vector[column])
            return values
        return self.content[row][column]


class RangeType(BaseType):
    def __init__(self, start, end):
        super().__init__("range")
        self.start = start
        self.end = end


class SpreadType(BaseType):
    def __init__(self, value):
        super().__init__("spread", shapeOfValue=(len(value),), content=value)


# class ViewType(BaseType):
#     def __init__(self, value, full_array):
#         super().__init__('view', typeOfValue=None, shapeOfValue=None, content=value)
#         self.full_array = full_array



class NodeVisitor(object):
    def visit(self, node):
        return node.visit(self)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.scopes = SymbolTable()
        self.typeTable = TypeTable()

    def visit_IntNum(self, node: IntNum):
        return ScalarType(node.typeOfValue, value=node.value)

    def visit_FloatNum(self, node: FloatNum):
        return ScalarType(node.typeOfValue, value=node.value)

    def visit_String(self, node: String):
        return ScalarType("string", value=node.value)

    def visit_Variable(self, node: Variable):
        id = self.scopes.get(node.name)
        if not id:
            return UndefinedType()
        return id

    def visit_BinExpr(self, node: BinExpr):
        left: BaseType = self.visit(node.left)
        if isinstance(left, ErrorType) or isinstance(left, UndefinedType):
            return left

        right: BaseType = self.visit(node.right)
        if isinstance(right, ErrorType) or isinstance(right, UndefinedType):
            return right

        if left.entityType != right.entityType:
            return ErrorType(
                f"Line {node.lineno}: cant do operations between {left.entityType} and {right.entityType}"
            )

        new_type = self.typeTable.getType(left.typeOfValue, node.op, right.typeOfValue)
        if not new_type:
            return ErrorType(
                f"Line {node.lineno}: cant do operation {left.typeOfValue} {node.op} {right.typeOfValue}"
            )

        if node.op in [">", "<", "==", ">=", "<=", "!="]:
            if isinstance(left, ScalarType):
                return ScalarType(new_type, value=None)
            return ErrorType(
                f"Line {node.lineno}: cannot compare {left.entityType} and {right.entityType}"
            )

        if isinstance(left, ScalarType):
            return ScalarType(new_type, value=None)

        if isinstance(left, VectorType):
            return VectorType(new_type, left.columns(), value=None)

        if isinstance(left, MatrixType) and isinstance(right, MatrixType):
            if "*" == node.op:
                if left.shapeOfValue[1] != right.shapeOfValue[0]:
                    return ErrorType(
                        f"Line {node.lineno}: cannot multiply matrices of shapes {left.shapeOfValue} and {right.shapeOfValue}"
                    )
            elif left.shapeOfValue != right.shapeOfValue:
                return ErrorType(
                    f"Line {node.lineno}: cannot do operation {node.op} on shapes {left.shapeOfValue} and {right.shapeOfValue}"
                )
            return MatrixType(new_type, left.rows(), right.columns(), value=None)

    def visit_Transpose(self, node: Transpose):
        entity = self.visit(node.expression)
        if isinstance(entity, ErrorType) or isinstance(entity, UndefinedType):
            return entity
        if isinstance(entity, VectorType):
            return entity

        if isinstance(entity, MatrixType):
            return MatrixType(
                entity.typeOfValue,
                columns=entity.rows(),
                rows=entity.columns(),
                value=None,
            )

        return ErrorType(f"Line {node.lineno}: cant transpose {entity.entityType}")

    def visit_Zeros(self, node: Zeros):
        sizes: list[BaseType] = [self.visit(size) for size in node.sizes]

        for size in sizes:
            if isinstance(size, ErrorType) or isinstance(size, UndefinedType):
                return size
            if not isinstance(size, ScalarType):
                return ErrorType(
                    f"Line {node.lineno}: size has to be scalar but is {size}"
                )
            if size.typeOfValue != "intnum":
                return ErrorType(
                    f"Line {node.lineno}: size has to be an intnum but is {size.typeOfValue}"
                )
        if len(sizes) > 1:
            return MatrixType(
                typeOfValue="intnum",
                rows=sizes[0].content,
                columns=sizes[1].content,
                value=None,
            )
        return MatrixType(
            typeOfValue="intnum",
            rows=sizes[0].content,
            columns=sizes[0].content,
            value=None,
        )

    def visit_Ones(self, node: Zeros):
        sizes: list[BaseType] = [self.visit(size) for size in node.sizes]

        for size in sizes:
            if isinstance(size, ErrorType) or isinstance(size, UndefinedType):
                return size
            if not isinstance(size, ScalarType):
                return ErrorType(
                    f"Line {node.lineno}: size has to be scalar but is {size}"
                )
            if size.typeOfValue != "intnum":
                return ErrorType(
                    f"Line {node.lineno}: size has to be an intnum but is {size.typeOfValue}"
                )
        if len(sizes) > 1:
            return MatrixType(
                typeOfValue="intnum",
                rows=sizes[0].content,
                columns=sizes[1].content,
                value=None,
            )
        return MatrixType(
            typeOfValue="intnum",
            rows=sizes[0].content,
            columns=sizes[0].content,
            value=None,
        )

    def visit_Eye(self, node: Zeros):
        sizes: list[BaseType] = [self.visit(size) for size in node.sizes]

        for size in sizes:
            if isinstance(size, ErrorType) or isinstance(size, UndefinedType):
                return size
            if not isinstance(size, ScalarType):
                return ErrorType(
                    f"Line {node.lineno}: size has to be scalar but is {size}"
                )
            if size.typeOfValue != "intnum":
                return ErrorType(
                    f"Line {node.lineno}: size has to be an intnum but is {size.typeOfValue}"
                )
        if len(sizes) > 1:
            return MatrixType(
                typeOfValue="intnum",
                rows=sizes[0].content,
                columns=sizes[1].content,
                value=None,
            )
        return MatrixType(
            typeOfValue="intnum",
            rows=sizes[0].content,
            columns=sizes[0].content,
            value=None,
        )

    def visit_Block(self, node: Block):
        self.scopes.pushScope()
        entity = self.visit(node.statement)
        if node.next_statements is not None:
            newEntity = self.visit(node.next_statements)
            if isinstance(newEntity, ErrorType) or isinstance(newEntity, UndefinedType):
                entity = newEntity
        self.scopes.popScope()
        return entity

    def visit_Statement(self, node: Statement):
        entity = self.visit(node.statement)
        if node.next_statements is not None:
            new_entity = self.visit(node.next_statements)
            if isinstance(new_entity, ErrorType) or isinstance(
                new_entity, UndefinedType
            ):
                entity = new_entity
        return entity

    def visit_Continue(self, _: Continue):
        if not self.scopes.isInsideLoop():
            return ErrorType(f"Line {_.lineno}: Continue is not inside loop")
        return SuccessType()

    def visit_Break(self, _: Break):
        if not self.scopes.isInsideLoop():
            return ErrorType(f"Line {_.lineno}: Break is not inside loop")
        return SuccessType()

    def visit_Return(self, node: Return):
        entity = self.visit(node.expression)
        if isinstance(entity, ErrorType) or isinstance(entity, UndefinedType):
            return entity
        return SuccessType()

    def visit_Assignment(self, node: Assignment):
        left = self.visit(node.variable)
        if isinstance(left, ErrorType):
            return left

        right = self.visit(node.value)
        if isinstance(right, ErrorType) or isinstance(right, UndefinedType):
            return right

        if node.op == "=":
            if not isinstance(node.variable, ArrayAccess):
                self.scopes.put(node.variable.name, right)
            elif left.typeOfValue != right.typeOfValue:
                return ErrorType(
                    f"Line {node.lineno}: cannot assign {right.typeOfValue} into {left.typeOfValue} matrix"
                )

        else:
            if isinstance(left, UndefinedType) or left.entityType != right.entityType:
                return ErrorType(
                    f"Line {node.lineno}: cannot do operation {left.entityType} {node.op} {right.entityType}"
                )
            
            new_type = self.typeTable.getType(
                left.typeOfValue, node.op[0], right.typeOfValue
            )

            if not new_type:
                return ErrorType(
                    f"Line {node.lineno}: cannot do operation {left.typeOfValue} {node.op} {right.typeOfValue}"
                )

            self.scopes.put(node.variable.name, right)
        return SuccessType()

    def visit_ArrayRange(self, node: ArrayRange):
        start = self.visit(node.start)
        if isinstance(start, ErrorType) or isinstance(start, UndefinedType):
            return start
        end = self.visit(node.end)
        if isinstance(end, ErrorType) or isinstance(end, UndefinedType):
            return end

        if isinstance(start, Variable):
            start = self.scopes.get(start.name)
            if start is None:
                return UndefinedType()

        if isinstance(end, Variable):
            end = self.scopes.get(end.name)
            if end is None:
                return UndefinedType()

        if isinstance(start, IntNum) and isinstance(end, IntNum):
            if start.value > end.value:
                return ErrorType(
                    f"Line {node.lineno}: start value {start.value} > end value {end.value}"
                )

        return RangeType(start=start, end=end)

    def visit_ForLoop(self, node: ForLoop):
        range_entity = self.visit(node.range)
        if isinstance(range_entity, ErrorType) or isinstance(
            range_entity, UndefinedType
        ):
            return range_entity
        self.scopes.put(
            node.variable.name, ScalarType("intnum", value=range_entity.start)
        )

        self.scopes.enterLoop()

        block = self.visit(node.block)

        if isinstance(block, ErrorType) or isinstance(block, UndefinedType):
            return block

        self.scopes.escapeLoop()

        return SuccessType()

    def visit_WhileLoop(self, node: WhileLoop):
        condition = self.visit(node.condition)
        if condition.typeOfValue != "boolean":
            return ErrorType(f"Line {node.lineno}: condition has to be boolean")

        self.scopes.enterLoop()

        block = self.visit(node.block)
        if isinstance(block, ErrorType) or isinstance(block, UndefinedType):
            return block

        self.scopes.escapeLoop()

        return SuccessType()

    def visit_IfElse(self, node: IfElse):
        condition = self.visit(node.condition)
        if condition.typeOfValue != "boolean":
            return ErrorType(f"Line {node.lineno}: condition has to be boolean")

        if_block = self.visit(node.if_block)
        if isinstance(if_block, ErrorType) or isinstance(if_block, UndefinedType):
            return if_block
        if node.else_block is not None:
            else_block = self.visit(node.else_block)
            if isinstance(else_block, ErrorType) or isinstance(
                else_block, UndefinedType
            ):
                return else_block
        return SuccessType()

    def visit_ArrayAccess(self, node: ArrayAccess):
        array = self.visit(node.array)
        if array.entityType != "matrix" and array.entityType != "vector":
            return ErrorType(f"Line {node.lineno}: cannot access {array.typeOfValue}")

        indexes = [self.visit(index) for index in node.indexes]

        if len(indexes) > 2:
            return ErrorType(
                f"Line {node.lineno}: cannot access {len(indexes)} indices"
            )

        if len(indexes) != 1 and array.entityType == "vector":
            return ErrorType(f"Line {node.lineno}: cannot access {array.typeOfValue}")

        if array.entityType == "matrix":
            if (
                array.shapeOfValue[0] > indexes[0].content >= 0
                and array.shapeOfValue[1] > indexes[1].content >= 0
            ):
                return ScalarType(
                    typeOfValue=array.typeOfValue,
                    value=array.valueAt(indexes[0], indexes[1]),
                )
            return ErrorType(
                f"Line {node.lineno}: indexes {indexes[0].content}, {indexes[1].content} out of range"
            )
        if array.entityType == "vector":
            if array.shapeOfValue[0] > indexes[0].content >= 0:
                return ScalarType(
                    typeOfValue=array.typeOfValue, value=array.valueAt(indexes[0])
                )
            return ErrorType(
                f"Line {node.lineno}: index {indexes[0].content} out of range"
            )

    def visit_Array(self, node: Array):
        val = self.visit(node.elements)

        if isinstance(val, ErrorType) or isinstance(val, UndefinedType):
            return val

        for i in range(1, len(val.content)):
            prev = val.content[i - 1]
            curr = val.content[i]
            if prev.typeOfValue != curr.typeOfValue:
                return ErrorType(
                    f"Line {node.lineno}: cannot create array with different value types"
                )
        typeOfContent = val.content[0].typeOfValue
        if node.other is not None:
            other = self.visit(node.other)
            if isinstance(other, ErrorType) or isinstance(other, UndefinedType):
                return other

            for i in range(1, len(other.content)):
                prev = other.content[i - 1]
                curr = other.content[i]
                if len(prev.content) != len(curr.content):
                    return ErrorType(f"Line {node.lineno}: incorrect matrix shape")
                if prev.typeOfValue != curr.typeOfValue:
                    return ErrorType(f"Line {node.lineno}: inconsistent matrix types")
            typeOfContent = other.content[0].content[0].typeOfValue
            return MatrixType(
                typeOfValue=typeOfContent,
                rows=1 + other.rows(),
                columns=other.columns(),
                value=[val] + other.content,
            )

        if typeOfContent is None:
            typeOfContent = val.content[0].content[0].typeOfValue
        return MatrixType(
            typeOfValue=typeOfContent, rows=1, columns=len(val.content), value=[val]
        )

    def visit_Spread(self, node: Spread):
        element = self.visit(node.element)
        if isinstance(element, ErrorType) or isinstance(element, UndefinedType):
            return element
        if node.next is not None:
            nextt: SpreadType = self.visit(node.next)
            if isinstance(nextt, ErrorType) or isinstance(nextt, UndefinedType):
                return nextt
            return SpreadType(value=[element] + nextt.content)
        return SpreadType(value=[element])

    def visit_Print(self, node: Print):
        elems = self.visit(node.expressions)
        if isinstance(elems, ErrorType) or isinstance(elems, UndefinedType):
            return elems
        return SuccessType()
