# Purpose: Constructs the desktop user interface components using Tkinter.
import tkinter as tk
from tkinter import messagebox
from config import BG_COLOR, HEADER_COLOR, BTN_SAVE_BG, BTN_MARK_BG, BTN_EXIT_BG
from validators import validate_inputs
from helpers import check_duplicate_registration
from face_engine import capture_and_save_face, recognize_face_and_log

class AttendanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("FaceVision AI")
        self.root.geometry("500x600")
        self.root.configure(bg=BG_COLOR)
        self.attendance_today = []
        self._build_ui()
    def _build_ui(self):
        # Header Label
        tk.Label(self.root, text="FaceVision AI", font=("Helvetica", 18, "bold"),
                 bg=BG_COLOR, fg=HEADER_COLOR).pack(pady=15)
        # Input Fields Frame
        input_frame = tk.Frame(self.root, bg=BG_COLOR)
        input_frame.pack(pady=5, anchor="w", padx=30)
        tk.Label(input_frame, text="Name:", bg=BG_COLOR, font=("Arial", 12)).grid(row=0, column=0, sticky="w", pady=5)
        self.name_input = tk.Entry(input_frame, width=30, font=("Arial", 12))
        self.name_input.grid(row=0, column=1, pady=5, padx=10)

        tk.Label(input_frame, text="UID (Roll No):", bg=BG_COLOR, font=("Arial", 12)).grid(row=1, column=0, sticky="w", pady=5)
        self.uid_input = tk.Entry(input_frame, width=30, font=("Arial", 12))
        self.uid_input.grid(row=1, column=1, pady=5, padx=10)
        # Action Buttons Frame
        button_frame = tk.Frame(self.root, bg=BG_COLOR)
        button_frame.pack(pady=10)
        tk.Button(button_frame, text="📷 Save Face", width=20, command=self.handle_save_face,
                  bg=BTN_SAVE_BG, font=("Arial", 11)).grid(row=0, column=0, padx=10, pady=5)        
        tk.Button(button_frame, text="☑ Mark Attendance", width=20, command=self.handle_mark_attendance,
                  bg=BTN_MARK_BG, font=("Arial", 11)).grid(row=0, column=1, padx=10, pady=5)        
        tk.Button(button_frame, text="❌ Exit", width=42, command=self.root.quit,
                  bg=BTN_EXIT_BG, font=("Arial", 11)).grid(row=1, column=0, columnspan=2, pady=10)
        # Attendance Listbox View
        tk.Label(self.root, text="Today's Attendance:", font=("Arial", 13, "bold"),
                 bg=BG_COLOR, fg="#444").pack(pady=(15, 5), anchor="w", padx=30)        
        self.listbox = tk.Listbox(self.root, width=60, height=12, font=("Courier", 10))
        self.listbox.pack(padx=30, pady=5, anchor="w")
    def handle_save_face(self):
        user_name = self.name_input.get().strip()
        user_uid = self.uid_input.get().strip()
        if not validate_inputs(user_name, user_uid):
            return
        if check_duplicate_registration(user_name, user_uid):
            messagebox.showwarning("Duplicate", "Same Name and UID already exist.")
            return
        capture_and_save_face(user_name, user_uid)
    def handle_mark_attendance(self):
        user_name = self.name_input.get().strip()
        user_uid = self.uid_input.get().strip()
        if not validate_inputs(user_name, user_uid):
            return
        recognize_face_and_log(user_name, user_uid, self.update_attendance_list)
    def update_attendance_list(self, uid, name, timestamp):
        entry = f"{uid} - {name} at {timestamp}"
        if entry not in self.attendance_today:
            self.attendance_today.append(entry)
            self.listbox.insert(tk.END, entry)