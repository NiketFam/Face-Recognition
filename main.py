# Purpose: Main application entry point.

import tkinter as tk
from helpers import initialize_environment
from gui import AttendanceApp

def main():
    initialize_environment()
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()



# ./venv/Scripts/python main.py