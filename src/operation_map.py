from dataclasses import dataclass, field

from src.type_checker import ScalarType, MatrixType


@dataclass
class OperationMap:
    operation_map: dict = field(
        default_factory=lambda: {
            "+": lambda x, y: x + y,
            "-": lambda x, y: x - y,
            "neg": lambda x: -x,
            "*": lambda x, y: x * y,
            "/": lambda x, y: x / y,
            ".+": matrix_add,
            ".-": matrix_sub,
            ".*": matrix_mul,  # element wise matrix multiplication
            "./": matrix_div,  # element wise matrix division
            "'": matrix_transpose,
            "<": lambda x, y: x < y,
            ">": lambda x, y: x > y,
            "<=": lambda x, y: x <= y,
            ">=": lambda x, y: x >= y,
            "==": lambda x, y: x == y,
            "!=": lambda x, y: x != y,
        }
    )


def matrix_add(matrix1, matrix2):
    n, m = len(matrix1.content), len(matrix1.content[0])
    result_matrix = [
        [
            ScalarType(
                matrix1.typeOfValue,
                matrix1.content[i][j].content + matrix2.content[i][j].content,
            )
            for j in range(m)
        ]
        for i in range(n)
    ]
    return MatrixType(matrix1.typeOfValue, n, m, result_matrix)


def matrix_sub(matrix1, matrix2):
    n, m = len(matrix1.content), len(matrix1.content[0])
    result_matrix = [
        [
            ScalarType(
                matrix1.typeOfValue,
                matrix1.content[i][j].content - matrix2.content[i][j].content,
            )
            for j in range(m)
        ]
        for i in range(n)
    ]
    return MatrixType(matrix1.typeOfValue, n, m, result_matrix)


def matrix_mul(matrix1, matrix2):
    n, m = len(matrix1.content), len(matrix1.content[0])
    result_matrix = [
        [
            ScalarType(
                matrix1.typeOfValue,
                matrix1.content[i][j].content * matrix2.content[i][j].content,
            )
            for j in range(m)
        ]
        for i in range(n)
    ]
    return MatrixType(matrix1.typeOfValue, n, m, result_matrix)


def matrix_div(matrix1, matrix2):
    n, m = len(matrix1.content), len(matrix1.content[0])
    result_matrix = [
        [
            ScalarType(
                matrix1.typeOfValue,
                matrix1.content[i][j].content / matrix2.content[i][j].content,
            )
            for j in range(m)
        ]
        for i in range(n)
    ]
    return MatrixType(matrix1.typeOfValue, n, m, result_matrix)


def matrix_transpose(matrix):
    n, m = len(matrix.content), len(matrix.content[0])
    transposed_matrix = [
        [ScalarType(matrix.typeOfValue, matrix.content[j][i].content) for j in range(n)]
        for i in range(m)
    ]
    return MatrixType(matrix.typeOfValue, m, n, transposed_matrix)
