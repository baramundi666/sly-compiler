
class Memory:
    def __init__(self, name: str): # memory name
        self.name = name
        self.scope = dict()

    def has_key(self, name):  # variable name
        return name in self.scope and self.scope[name] is not None

    def get(self, name):         # gets from memory current value of variable <name>
        if self.has_key(name):
            return self.scope[name]
        return None

    def put(self, name, value):  # puts into memory current value of variable <name>
        self.scope[name] = value


class MemoryStack:
    def __init__(self, memory=None): # initialize memory stack with memory <memory>
        self.memory_stack = []
        self.top_memory = None
        if memory is not None:
            self.push(memory)

    def get(self, name):             # gets from memory stack current value of variable <name>
        if self.top_memory.has_key(name):
            return self.top_memory.get(name)

    def insert(self, name, value): # inserts into memory stack variable <name> with value <value>
        self.top_memory.put(name, value)

    def set(self, name, value): # sets variable <name> to value <value>
        self.top_memory.put(name, value)

    def push(self, memory: Memory): # pushes memory <memory> onto the stack
        self.memory_stack.append(memory)
        self.top_memory = memory

    def pop(self):          # pops the top memory from the stack
        self.memory_stack.pop()
        self.top_memory = self.memory_stack[-1]

