class Task:
    def __init__(self, description, start_time, end_time, priority):
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.priority = priority

    def __str__(self):
        return f"{self.description} | {self.start_time} - {self.end_time} | Priority: {self.priority}"


class AVLNode:
    def __init__(self, task):
        self.task = task
        self.left = None
        self.right = None
        self.height = 1


class AvlTree:
    def insert(self, root, task):
        if not root:
            return AVLNode(task)

        if task.priority < root.task.priority:
            root.left = self.insert(root.left, task)
        else:
            root.right = self.insert(root.right, task)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        balance = self.get_balance(root)

        if balance > 1 and task.priority < root.left.task.priority:
            return self.right_rotate(root)
        if balance < -1 and task.priority > root.right.task.priority:
            return self.left_rotate(root)
        if balance > 1 and task.priority > root.left.task.priority:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)
        if balance < -1 and task.priority < root.right.task.priority:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root

    def left_rotate(self, z):
        y = z.right
        T2 = y.left
        y.left = z
        z.right = T2
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right
        y.right = z
        z.left = T3
        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        return y

    def get_height(self, root):
        return 0 if not root else root.height

    def get_balance(self, root):
        return 0 if not root else self.get_height(root.left) - self.get_height(root.right)

    def inorder(self, root):
        if not root:
            return []
        return self.inorder(root.left) + [root.task] + self.inorder(root.right)

    def display(self, root):
        tasks = self.inorder(root)
        for task in tasks:
            print(task)
