from dataclasses import dataclass, field


@dataclass
class OperationMap:
    operation_map: dict = field(default_factory=lambda:
    {
        "+": lambda x, y: x + y,
        "-": lambda x, y: x - y,
        "neg": lambda x: -x,
        "*": lambda x, y: x * y,
        "/": lambda x, y: x / y,
        ".+": matrix_add,
        ".-": matrix_sub,
        ".*": matrix_mul,
        "./": matrix_div,
        "'": matrix_transpose,
        "<": lambda x, y: x < y,
        ">": lambda x, y: x > y,
        "<=": lambda x, y: x <= y,
        ">=": lambda x, y: x >= y,
        "==": lambda x, y: x == y,
        "!=": lambda x, y: x != y,
    })

def matrix_add(matrix1, matrix2):
    n, m = len(matrix1), len(matrix1[0])
    result_matrix = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            result_matrix[i][j] = matrix1[i][j] + matrix2[i][j]
    return result_matrix

def matrix_sub(matrix1, matrix2):
    n, m = len(matrix1), len(matrix1[0])
    result_matrix = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            result_matrix[i][j] = matrix1[i][j] - matrix2[i][j]
    return result_matrix

def matrix_mul(matrix, scalar):
    n, m = len(matrix), len(matrix[0])
    result_matrix = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            result_matrix[i][j] = matrix[i][j] * scalar
    return result_matrix

def matrix_div(matrix, scalar):
    n, m = len(matrix), len(matrix[0])
    result_matrix = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            result_matrix[i][j] = matrix[i][j] / scalar
    return result_matrix

def matrix_transpose(matrix):
    n, m = len(matrix), len(matrix[0])
    transposed_matrix = [[0 for _ in range(n)] for _ in range(m)]
    for i in range(n):
        for j in range(m):
            transposed_matrix[j][i] = matrix[i][j]
    return transposed_matrix