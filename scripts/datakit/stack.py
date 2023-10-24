class Stack:
    def __init__(self):
        self._stack = []
    
    def stack(self):
        return self._stack
    
    def push(self, item):
        self._stack.append(item)
    
    def pop(self):
        return self._stack.pop()
    
    def peek(self):
        return self._stack[-1]
    
    def __len__(self):
        return len(self._stack)