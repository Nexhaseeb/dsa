#stack.py
class Stack:
    def __init__(self):
        self.stack = []

    def push(self, task):
        self.stack.append(task)

    def pop(self):
        if not self.is_empty():
            return self.stack.pop()
        return None

    def is_empty(self):
        return len(self.stack) == 0

    def display(self):
        for task in reversed(self.stack):
            print(f"Undo Task: {task.description} | {task.start_time} - {task.end_time} | Priority: {task.priority}")
