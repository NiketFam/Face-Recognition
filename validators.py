# Purpose: Handles input validation using Regular Expressions.

import re
from tkinter import messagebox

def validate_inputs(name: str, uid: str) -> bool:
    """
    Validates user name and UID using strict regex patterns.
    - Name: Alphabets and spaces only.
    - UID: Standardized institutional format (e.g., 23BCS10095).
    """
    name_valid = bool(re.fullmatch(r"[A-Za-z ]+", name))
    uid_valid = bool(re.fullmatch(r"\d{2}[A-Za-z]{3}\d{5}", uid))

    if not name or not uid:
        messagebox.showwarning("Missing Info", "Please enter both Name and UID.")
        return False

    if not name_valid:
        messagebox.showwarning("Invalid Name", "Name should only contain alphabets and spaces.")
        return False

    if not uid_valid:
        messagebox.showwarning("Invalid UID", "UID must be in format like 24BCS0020, 23BDM12534, etc.")
        return False

    return True