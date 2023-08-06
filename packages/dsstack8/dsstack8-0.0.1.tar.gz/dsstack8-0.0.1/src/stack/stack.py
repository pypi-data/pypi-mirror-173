class Stack:
    def __init__(self):
        self.stack = []
        self.length = 0

    def push(self, element):
        self.stack.append(element)
        self.length += 1

    def remove(self):
        self.stack.pop()
        self.length -= 1

    def peek(self):
        if self.length == 0:
            return "Stack is Empty..."
        return self.stack[self.length-1]

    def print_stack(self):
        reversed_list = []
        output = ""
        for i in self.stack:
            reversed_list.insert(0,i)
        for i in reversed_list:
            output += f"\n|{i}|"  
        output += "\n ‾"
        return output
