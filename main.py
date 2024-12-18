from datetime import datetime, timedelta, timezone
from dateutil.parser import parse
import pytz
import time
from queue import Queue
utc = pytz.utc
now = datetime.now(utc) 
class Task:
    def __init__(self,task_number, description, start_time, end_time, priority,task_duration):
        self.task_number = task_number
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.priority = priority
        self.task_duration = task_duration
            
    def getStarTime(self):
       return self.start_time
    def getEndTime(self):
        return self.end_time
    
    def modifydata(self):
        print("1.Task number \n2.Task description \n3.Start Time \n4.End Time \n5.Priority \n6.Task Duration")
        choice = input("Enter detail number to modify :")
        if choice == 1:
            task_number = input("Change  task number to : ")
            self.task_number = task_number
        if choice == 2:
            description = input("Change task description to : ")
            self.description = description
        if choice == 3:
            start_time = input("Change start time to --(YYYY-MM-DD HH:MM:SS): ")
            self.start_time = start_time
        if choice == 4:
            end_time = input("Change end time to --(YYYY-MM-DD HH:MM:SS): ")
            self.end_time = end_time
        if choice == 5:
            priority = int(input("Change priority (lowest number = higher priority): "))
            self.priority = priority
        if choice == 6:
            task_duration = input("Change time duration to--(HH:MM:SS): ")
            self.task_duration = task_duration
        

        print("Updated Details--")
        print(f"Task Number {self.task_number} | {self.description} | {self.start_time} - {self.end_time} | Priority: {self.priority} | Task Duration: {self.task_duration}")

    

    def __str__(self):
        return f"{self.task_number} | {self.description} | {self.start_time} - {self.end_time} | Priority: {self.priority} | Task Duration: {self.task_duration}"


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
    def add_in_queue(self,task_queue,root):
        tasks = self.inorder(root)
        for task in tasks:
            task_queue.put(task)
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
    def clear_linked_list(self):
        # Simply set the head to None to clear the list
        self.head = None
                    
    def insert_in_order(self, task):
        new_node = Node(task)
        # If the new list is empty or the task should be placed at the head
        if not self.head or datetime.strptime(task.start_time, "%Y-%m-%d %H:%M:%S") < datetime.strptime(self.head.task.start_time, "%Y-%m-%d %H:%M:%S"):
            new_node.next = self.head
            self.head = new_node
            return

        # Otherwise, insert the task in the correct position based on start_time
        current = self.head
        while current.next and datetime.strptime(task.start_time, "%Y-%m-%d %H:%M:%S") >= datetime.strptime(current.next.task.start_time, "%Y-%m-%d %H:%M:%S"):
            current = current.next
        new_node.next = current.next
        current.next = new_node

    def filter_tasks_after_current_time(self, current_time, ew_linked_list):
        current = self.head
        karachi_tz = pytz.timezone('Asia/Karachi')

        # Use current_time to set the end of the day to 23:59:59 of today
        #end_of_day = karachi_tz.localize(datetime(current_time.year, current_time.month, current_time.day, 23, 59, 59))
        
        

        while current:
            # Parse the task start time
            task_start_time = current.task.start_time
            #task_start_time = karachi_tz.localize(task_start_time)
            #task_start_time = karachi_tz.localize(task_start_time.replace(year=current_time.year, month=current_time.month, day=current_time.day))  # Localize with today's date
            # print(f"\r[{task_start_time.strftime('%Y-%m-%d %H:%M:%S')}] Task {end_of_day.strftime('%Y-%m-%d %H:%M:%S')} completed.")
            # Check if the task's start time is after the current time and before midnight (23:59:59)
            if task_start_time > current_time:
                #print("yes")
                ew_linked_list.insert_in_order(current.task)
            current = current.next

    def execute_tasks(self, current_time, list):
        karachi_tz = pytz.timezone('Asia/Karachi')
    
        # Ensure current_time is timezone-aware
        if current_time.tzinfo is None:
            current_time = karachi_tz.localize(current_time)
        
        current = list.head  # Start from the head of the new linked list
    
        while current:
            task_start_time = current.task.start_time
            task_end_time = current.task.end_time
    
            # Ensure task start and end times are timezone-aware
            if task_start_time.tzinfo is None:
                task_start_time = karachi_tz.localize(task_start_time)
            if task_end_time.tzinfo is None:
                task_end_time = karachi_tz.localize(task_end_time)
            
            print(f"\rStart Time: [{task_start_time.strftime('%Y-%m-%d %H:%M:%S')}]")
            
            print(f"\r[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Waiting for task to start: {current.task.description}...", end="")
            
            # Wait until the task start time
            while task_start_time > current_time:
                print("Waiting for task to start...")  # Debug statement
                time.sleep(1)  # Wait a second before checking again
                current_time = datetime.now(karachi_tz)  # Update current time for the check
                print(f"\r[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Waiting for task to start: {current.task.description}...", end="")
            
            # Now that we've passed the start time, execute the task
            print(f"\r[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Executing task: {current.task.description}, Start Time: {task_start_time.strftime('%Y-%m-%d %H:%M:%S')} - End Time: {task_end_time.strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Simulate task execution for task duration
            while current_time < task_end_time:    
                time.sleep(1)
                current_time = datetime.now(karachi_tz)  # Update current time during task execution
            # Update current time every second during task execution
                print(f"\r[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Executing task: {current.task.description}, Start Time: {task_start_time.strftime('%Y-%m-%d %H:%M:%S')} - End Time: {task_end_time.strftime('%Y-%m-%d %H:%M:%S')}", end="")
            
            print(f"\r[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Task {current.task.description} completed.")
            
            # Move to the next task
            current = current.next



    
        # Once all tasks are completed, clear the linked list
        self.clear_linked_list()
        print("All tasks have been executed. Linked list has been cleared.")


    def delete(self, tasknumber):
        current = self.head
        prev = None
        while current:
            if current.task.task_number == tasknumber:
                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next
                return True
            prev = current
            current = current.next
        return False
    def findtask(self,num):
        current = self.head
        while current:
            if current.task.task_number == num:
                print(f"{current.task.description} | {current.task.start_time} - {current.task.end_time} | Priority: {current.task.priority}")
            current = current.next
        
        
    def display(self):
        current = self.head
        while current:
            print(f"{current.task.description} | {current.task.start_time} - {current.task.end_time} | Priority: {current.task.priority}")
            current = current.next

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

def main():
    linked_list = LinkedList()
    avl_tree = AvlTree()
    root = None  # Track AVL tree root
    task_queue = Queue()
    stack = Stack()
    karachi_tz = pytz.timezone('Asia/Karachi')

    while True:
        print("\nMenu:")
        print("1. Add Task")
        print("2. Delete Task")
        print("3. Modify Task")
        print("4. Display All Tasks")
        print("5. Start task according to time decided")
        print("6. Start Task by Pirority")
        print("7. Undo Last Change (Stack)")
        print("8. Exit")

        choice = int(input("Enter choice: "))

        if choice == 1:
            task_number = input("Enter task number: ")
            description = input("Enter task description: ")
            start_time = input("Enter start time (YYYY-MM-DD HH:MM:SS): ")
            end_time = input("Enter end time (YYYY-MM-DD HH:MM:SS): ")
            priority = int(input("Enter priority (lowest number = higher priority): "))
            task_duration = input("Set time duration(HH:MM:SS): ")
            h, m, s = map(int, task_duration.split(":"))
            # Convert to total seconds
            task_duration = h * 3600 + m * 60 + s
            start_time = utc.localize(datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S"))
            end_time = utc.localize(datetime.strptime(end_time, "%Y-%m-%d %H:%M:%S"))


            task = Task(task_number,description, start_time, end_time, priority,task_duration)
            linked_list.append(task)
            root = avl_tree.insert(root, task)  # Update the AVL tree root
            print("Task added.")

        elif choice == 2:
            task_number = input("Enter task number to delete: ")
            if linked_list.delete(task_number):
                print("Task deleted.")
            else:
                print("Task not found.")

        elif choice == 3:
            number = input("Enter the task number you want to modify")
            linked_list.findtask(number)
        
            # print("Modify task logic not implemented yet.")

        elif choice == 4:
            print("Displaying tasks in linked list:")
            linked_list.display()

        elif choice == 5:
            karachi_tz = pytz.timezone('Asia/Karachi')
            current_time = datetime.now(karachi_tz)
            ew_linked_list = LinkedList()
            current_time = datetime.now(karachi_tz)# Assume current time is 12:00:00
            linked_list.filter_tasks_after_current_time(current_time, ew_linked_list)# Filter tasks and store in new linked list
            
            #ew_linked_list.display()
            ew_linked_list.execute_tasks(current_time, ew_linked_list)
            



        elif choice == 6:
            task_queue = Queue()
            avl_tree.add_in_queue(task_queue,root)
            print("1. Start task now")
            choice = input("2. Enter start time manually")
            print("Starting task processing...")
 
            if choice == 1:
                while not task_queue.empty():
                    current_time = datetime.now(karachi_tz)  # Use timezone-aware datetime
                    current_task = task_queue.queue[0]  # Peek at the next task
                    end = karachi_tz.localize(end)
                    end = current_time + timedelta(seconds=current_task.task_duration)
                    print(f"[   ||  {current_task.description} || \nTask Started At: {current_time.strftime('%Y-%m-%d %H:%M:%S')} -|- Task Ends At: {end.strftime('%Y-%m-%d %H:%M:%S')} ]")
            
                    # Check if the task has finished
                    while current_time < end:  # Continue while current time is less than the end time
                        current_time = datetime.now(karachi_tz)  # Update current time for the check
                        
                        print(f"\r[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Waiting for {current_task.description} to finish...", end="")
                        time.sleep(1)  # Wait a second before checking again
                    finished_task = task_queue.get()  # Dequeue the task
                    print(f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Completed Task: {finished_task.description}")
                print("\nAll tasks have been completed.")
            else:
                    start = input("Enter the Time you want to start your tasks (YYYY-MM-DD HH:MM:SS): ")

    # Ensure start is a naive datetime before localization
                    start = datetime.strptime(start, "%Y-%m-%d %H:%M:%S")

                    if start.tzinfo is None:  # If naive, localize it
                        start = karachi_tz.localize(start)
                    else:
                        #print("The provided time is already timezone-aware. Localizing to Karachi time.")
                        start = start.astimezone(karachi_tz)
                    
                    current_time = datetime.now(karachi_tz)
                    while current_time < start:
                        current_time = datetime.now(karachi_tz)
                        print(f"\r[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Waiting for upcoming tasks to Start...", end="")
                        time.sleep(1)
                    while not task_queue.empty():
                        current_time = datetime.now(karachi_tz)  # Use timezone-aware datetime
                        current_task = task_queue.queue[0]  # Peek at the next task
                        end = current_time + timedelta(seconds=current_task.task_duration)
                        print(f"[   ||  {current_task.description} || \nTask Started At: {current_time.strftime('%Y-%m-%d %H:%M:%S')} -|- Task Ends At: {end.strftime('%Y-%m-%d %H:%M:%S')} ]")
                
                        # Check if the task has finished
                        while current_time < end:  # Continue while current time is less than the end time
                            current_time = datetime.now(karachi_tz)  # Update current time for the check
                            
                            print(f"\r[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Waiting for {current_task.description} to finish...", end="")
                            time.sleep(1)  # Wait a second before checking again
                        finished_task = task_queue.get()  # Dequeue the task
                        print(f"[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Completed Task: {finished_task.description}")
                    print("\nAll tasks have been completed.")

            
            

            
            

        elif choice == 7:
            print("Undoing last operation:")
            stack.display()

        elif choice == 8:
            break

if __name__ == "__main__":
    main()
