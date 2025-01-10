class VariableSymbol(object):
    def __init__(self, name, typeOfVariable):
        self.name = name
        self.typeOfVariable = typeOfVariable


class SymbolTable(object):
    def __init__(self):  # parent scope and symbol table name
        self.scopes = [{}]
        self.loopDepth = 0

    def put(
        self, name, typeOfValue
    ):  # put variable symbol or fundef under <name> entry
        self.scopes[-1][name] = typeOfValue

    def get(self, name):  # get variable symbol or fundef from <name> entry
        for scope_idx in range(len(self.scopes) - 1, -1, -1):
            if name in self.scopes[scope_idx]:
                return self.scopes[scope_idx][name]
        return None

    def erase(self, name):
        if name is None:
            return
        for scope_idx in range(len(self.scopes) - 1, -1, -1):
            if name in self.scopes[scope_idx]:
                del self.scopes[scope_idx][name]

    def pushScope(self):
        self.scopes.append({})

    def popScope(self):
        self.scopes.pop()

    def enterLoop(self):
        self.loopDepth += 1

    def escapeLoop(self):
        self.loopDepth -= 1

    def isInsideLoop(self):
        return self.loopDepth > 0


class TypeTable(object):
    def __init__(self):
        self.typeTable = {}

        self.typeTable["+"] = {}
        self.typeTable["+"]["intnum"] = {}
        self.typeTable["+"]["intnum"]["intnum"] = "intnum"
        self.typeTable["+"]["intnum"]["floatnum"] = "floatnum"
        self.typeTable["+"]["floatnum"] = {}
        self.typeTable["+"]["floatnum"]["intnum"] = "floatnum"
        self.typeTable["+"]["floatnum"]["floatnum"] = "floatnum"
        self.typeTable["+"]["string"] = {}
        self.typeTable["+"]["string"]["string"] = "string"

        self.typeTable["-"] = {}
        self.typeTable["-"]["intnum"] = {}
        self.typeTable["-"]["intnum"]["intnum"] = "intnum"
        self.typeTable["-"]["intnum"]["floatnum"] = "floatnum"
        self.typeTable["-"]["floatnum"] = {}
        self.typeTable["-"]["floatnum"]["intnum"] = "floatnum"
        self.typeTable["-"]["floatnum"]["floatnum"] = "floatnum"

        self.typeTable["*"] = {}
        self.typeTable["*"]["intnum"] = {}
        self.typeTable["*"]["intnum"]["intnum"] = "intnum"
        self.typeTable["*"]["intnum"]["floatnum"] = "floatnum"
        self.typeTable["*"]["intnum"]["string"] = "string"
        self.typeTable["*"]["floatnum"] = {}
        self.typeTable["*"]["floatnum"]["intnum"] = "floatnum"
        self.typeTable["*"]["floatnum"]["floatnum"] = "floatnum"
        self.typeTable["*"]["string"] = {}
        self.typeTable["*"]["string"]["intnum"] = "string"

        self.typeTable["/"] = {}
        self.typeTable["/"]["intnum"] = {}
        self.typeTable["/"]["intnum"]["intnum"] = "floatnum"
        self.typeTable["/"]["intnum"]["floatnum"] = "floatnum"
        self.typeTable["/"]["floatnum"] = {}
        self.typeTable["/"]["floatnum"]["intnum"] = "floatnum"
        self.typeTable["/"]["floatnum"]["floatnum"] = "floatnum"

        self.typeTable[".+"] = self.typeTable["+"]
        self.typeTable[".-"] = self.typeTable["-"]
        self.typeTable[".*"] = self.typeTable["*"]
        self.typeTable["./"] = self.typeTable["/"]

        self.typeTable["<"] = {}
        self.typeTable["<"]["intnum"] = {}
        self.typeTable["<"]["intnum"]["intnum"] = "boolean"
        self.typeTable["<"]["intnum"]["floatnum"] = "boolean"
        self.typeTable["<"]["floatnum"] = {}
        self.typeTable["<"]["floatnum"]["intnum"] = "boolean"
        self.typeTable["<"]["floatnum"]["floatnum"] = "boolean"

        self.typeTable[">"] = self.typeTable["<"]
        self.typeTable["<="] = self.typeTable["<"]
        self.typeTable[">="] = self.typeTable["<"]
        self.typeTable["=="] = self.typeTable["<"]
        self.typeTable["!="] = self.typeTable["<"]

    def getType(self, leftType, action, rightType):
        action = action.replace("=", "") if action[0] in "+-*/" else action
        if action not in self.typeTable:
            # print(f"unknown action {action}")
            return None
        if leftType not in self.typeTable[action]:
            # print(f"illegal left type {leftType} {action}")
            return None
        if rightType not in self.typeTable[action][leftType]:
            # print(f"illegal right type {leftType} {action} {rightType}")
            return None
        return self.typeTable[action][leftType][rightType]
