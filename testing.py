from datetime import datetime
import pytz
import time  # For simulating real-time task execution

class Task:
    def __init__(self, task_number, description, start_time, end_time, priority, task_duration):
        self.task_number = task_number
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.priority = priority
        self.task_duration = task_duration

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

    def filter_tasks_after_current_time(self, current_time, new_linked_list):
        current = self.head
        karachi_tz = pytz.timezone('Asia/Karachi')

        # Use current_time to set the end of the day to 23:59:59 of today
        end_of_day = karachi_tz.localize(datetime(current_time.year, current_time.month, current_time.day, 23, 59, 59))

        while current:
            # Parse the task start time
            task_start_time = datetime.strptime(current.task.start_time, "%Y-%m-%d %H:%M:%S")
            task_start_time = karachi_tz.localize(task_start_time.replace(year=current_time.year, month=current_time.month, day=current_time.day))  # Localize with today's date
            
            # Check if the task's start time is after the current time and before midnight (23:59:59)
            if task_start_time > current_time and task_start_time < end_of_day:
                new_linked_list.insert_in_order(current.task)
            current = current.next

    def execute_tasks(self, current_time, task_list):
        karachi_tz = pytz.timezone('Asia/Karachi')
        end_of_day = karachi_tz.localize(datetime(current_time.year, current_time.month, current_time.day, 23, 59, 59))
        
        # Ensure current_time is timezone-aware
        if current_time.tzinfo is None:
            current_time = karachi_tz.localize(current_time)
        
        current = task_list.head  # Start from the head of the new linked list
        
        # Directly print task details without needing a display method
        latest_end_time = None  # Initialize latest_end_time
    
        # Iterate through the linked list to get the latest task end time
        while current:
            task_end_time = current.task.end_time
            if isinstance(task_end_time, str):
            # Assuming the string is in the format 'YYYY-MM-DD HH:MM:SS'
                task_end_time = datetime.strptime(task_end_time, '%Y-%m-%d %H:%M:%S')
                task_end_time = karachi_tz.localize(task_end_time)  # Localize to Karachi time

            
            # Ensure task end time is timezone-aware
            if task_end_time.tzinfo is None:
                task_end_time = karachi_tz.localize(task_end_time)
            
            # Update the latest_end_time to the maximum end time
            if latest_end_time is None or task_end_time > latest_end_time:
                latest_end_time = task_end_time
            
            current = current.next  # Move to the next task in the list
    
        # Check if the list is empty or no valid task end time was found
        if latest_end_time is None:
            print("No tasks to execute.")
            return  # Exit if no tasks are present
        
        # Begin the task checking loop
        while current_time <= latest_end_time and current_time <= end_of_day:
            print(f"\r[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Checking for tasks...", end="")
            
            # Print updates every second until the last task end time is reached or end of day
            time.sleep(1)  # Wait for 1 second before checking again
            current_time = datetime.now(karachi_tz)  # Update current time to Karachi time
            
        if current_time > latest_end_time:
            print(f"\n[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] All tasks are completed.")
        elif current_time >= end_of_day:
            print("\nToday’s tasks reset.")
            
        

        


    def display(self):
        current = self.head
        while current:
            print(f"{current.task.description} | {current.task.start_time} - {current.task.end_time} | Priority: {current.task.priority}")
            current = current.next
        print("all data printed")

# Example usage:
# Creating a LinkedList with tasks
task1 = Task(1, "Task 1", "2024-12-19 13:29:30", "2024-12-19 13:29:50", 1, 1)  # Task duration 1 minute
task2 = Task(2, "Task 2", "2024-12-19 10:10:00", "2024-12-19 10:30:00", 2, 2)  # Task duration 2 minutes
task3 = Task(3, "Task 3", "2024-12-19 10:20:00", "2024-12-19 10:20:00", 3, 1)   # Task duration 1 minute
task4 = Task(4, "Task 4", "2024-12-19 10:45:50", "2024-12-19 10:46:20", 2, 1)   # Task duration 1 minute

original_linked_list = LinkedList()
original_linked_list.append(task1)
original_linked_list.append(task2)
original_linked_list.append(task3)
original_linked_list.append(task4)

# Add tasks to the new linked list after filtering them based on current time
new_linked_list = LinkedList()
karachi_tz = pytz.timezone('Asia/Karachi')
current_time = datetime.now(karachi_tz)

# Filter tasks based on current time
original_linked_list.filter_tasks_after_current_time(current_time, new_linked_list)

# Display the tasks in the new linked list
new_linked_list.display()

# Execute tasks
new_linked_list.execute_tasks(current_time, new_linked_list)
