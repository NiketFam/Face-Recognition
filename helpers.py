# Purpose: Initializes database directories and handles CSV file logging operations.
import os
import csv
from datetime import datetime
from config import FACE_DIR, ATTENDANCE_FILE

def initialize_environment():
    """Ensures required database directories and CSV header files exist."""
    if not os.path.exists(FACE_DIR):
        os.makedirs(FACE_DIR)

    if not os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "w", newline="") as f:
            csv.writer(f).writerow(["UID", "Name", "Timestamp"])

def already_marked(uid: str) -> bool:
    """Checks if the user has already been marked present on the current date."""
    today = datetime.now().strftime("%Y-%m-%d")
    if os.path.exists(ATTENDANCE_FILE):
        with open(ATTENDANCE_FILE, "r") as file:
            reader = csv.reader(file)
            for row in reader:
                if row and row[0] == uid and today in row[2]:
                    return True
    return False

def check_duplicate_registration(user_name: str, user_uid: str) -> bool:
    """Checks if the Name and UID combination is already registered in the face database."""
    for f in os.listdir(FACE_DIR):
        if f.endswith(".jpg"):
            parts = f.split('_')
            if len(parts) >= 2:
                existing_uid, existing_name = parts[0], parts[1]
                if existing_name.lower() == user_name.lower() and existing_uid == user_uid:
                    return True
    return False