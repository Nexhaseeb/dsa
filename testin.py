import time
from datetime import datetime
import pytz

# Input the start time
start_input = input("Enter the Time you want to start your tasks (YYYY-MM-DD HH:MM:SS): ")

# Parse the input and localize to UTC+5 (Asia/Karachi)
karachi_tz = pytz.timezone('Asia/Karachi')

# Convert the start time to Asia/Karachi time zone
start = datetime.strptime(start_input, "%Y-%m-%d %H:%M:%S")
start = karachi_tz.localize(start)  # Localize to Karachi time zone

# Get the current time in Asia/Karachi time zone
current_time = datetime.now(karachi_tz)

# Debug: Print the start and current times in Karachi time zone
print(f"Start time: {start.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Current time: {current_time.strftime('%Y-%m-%d %H:%M:%S')}")

# Check if the start time is in the future
if current_time < start:
    print("Waiting for the start time...")
    # Wait for the start time
    while current_time < start:
        current_time = datetime.now(karachi_tz)  # Update current time in Karachi time zone
        print(f"\r[{current_time.strftime('%Y-%m-%d %H:%M:%S')}] Waiting for upcoming tasks to Start...", end="")
        time.sleep(1)
else:
    print("The start time has already passed. Proceeding with task execution...")

# Task processing code would go here
