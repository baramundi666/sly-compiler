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
