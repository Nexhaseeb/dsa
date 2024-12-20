#link_list.py
class Node:
    def __init__(self, task):
        self.task = task
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, task):
        new_node = Node(task)
        if not self.head:
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node

    def delete(self, task_description):
        current = self.head
        prev = None
        while current:
            if current.task.description == task_description:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True
            prev = current
            current = current.next
        return False

    def display(self):
        current = self.head
        while current:
            print(f"{current.task.description} | {current.task.start_time} - {current.task.end_time} | Priority: {current.task.priority}")
            current = current.next
