class Stack:
    def __init__(self):
        self.array = []

    def push(self, item):
        self.array.append(item)

    def pop(self):
        if len(self.array) == 0:
            raise IndexError
        return self.array.pop()

    def peek(self):
        if len(self.array) == 0:
            raise IndexError
        return self.array[-1]

    def size(self):
        return len(self.array)

    def clear(self):
        self.array = []