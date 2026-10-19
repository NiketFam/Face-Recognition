import cv2
import cv2.data
import os
import time
import csv
from datetime import datetime
from tkinter import messagebox
from config import FACE_DIR, ATTENDANCE_FILE, MATCH_THRESHOLD, CAMERA_TIMEOUT, STABLE_CAPTURE_DELAY
from helpers import already_marked

def load_cascade():
    """Loads Haar Cascade by passing the XML path directly into the constructor."""
    xml_filename = "haarcascade_frontalface_default.xml"
    
    # Check if a local copy exists first, otherwise use cv2.data
    if os.path.exists(xml_filename):
        cascade_path = os.path.abspath(xml_filename)
    else:
        cascade_path = cv2.data.haarcascades + xml_filename

    # Pass the path directly into CascadeClassifier
    return cv2.CascadeClassifier(cascade_path)

def capture_and_save_face(user_name: str, user_uid: str):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Camera Error", "Cannot access webcam.")
        return

    detector = load_cascade()
    if detector.empty():
        messagebox.showerror("Classifier Error", "Could not load haarcascade_frontalface_default.xml file.")
        cap.release()
        return

    captured = False
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            if not captured and (time.time() - start_time > STABLE_CAPTURE_DELAY):
                face = gray[y:y+h, x:x+w]
                filename = f"{FACE_DIR}/{user_uid}_{user_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
                cv2.imwrite(filename, face)
                captured = True
                messagebox.showinfo("Captured", f"Face image saved successfully:\n{filename}")
                break

        cv2.putText(frame, f"Capturing {user_name} ({user_uid})", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (100, 255, 100), 2)
        cv2.imshow("Face Capture", frame)

        if captured or (cv2.waitKey(1) & 0xFF == 27):
            break

    cap.release()
    cv2.destroyAllWindows()

def recognize_face_and_log(user_name: str, user_uid: str, ui_callback):
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        messagebox.showerror("Camera Error", "Cannot access webcam.")
        return

    detector = load_cascade()
    if detector.empty():
        messagebox.showerror("Classifier Error", "Could not load haarcascade_frontalface_default.xml file.")
        cap.release()
        return

    known_faces = {}

    for img in os.listdir(FACE_DIR):
        path = os.path.join(FACE_DIR, img)
        if img.endswith(".jpg") and os.path.isfile(path):
            parts = img.split('_')
            if len(parts) >= 2:
                uid, name = parts[0], parts[1]
                image = cv2.imread(path, 0)
                known_faces[img] = (uid, name, image)

    matched = False
    start_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = detector.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=4, minSize=(30, 30))

        for (x, y, w, h) in faces:
            detected = gray[y:y+h, x:x+w]

            for filename, (uid, name, stored) in known_faces.items():
                try:
                    resized = cv2.resize(detected, (stored.shape[1], stored.shape[0]))
                    result = cv2.matchTemplate(resized, stored, cv2.TM_CCOEFF_NORMED)
                    _, score, _, _ = cv2.minMaxLoc(result)

                    if score > MATCH_THRESHOLD:
                        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        if not already_marked(uid):
                            with open(ATTENDANCE_FILE, "a", newline="") as f:
                                csv.writer(f).writerow([uid, name, current_time])
                            ui_callback(uid, name, current_time)
                            messagebox.showinfo("Attendance Marked", f"Marked attendance for:\nName: {name}\nUID: {uid}")
                        else:
                            messagebox.showinfo("Already Marked", f"{name} (UID {uid}) already marked today.")
                        matched = True
                        break
                except Exception as e:
                    print("Matching Error:", e)

            if matched:
                break

        cv2.putText(frame, "Looking for registered faces...", (15, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 200, 255), 2)
        cv2.imshow("Attendance Scanner", frame)

        if matched or (time.time() - start_time > CAMERA_TIMEOUT) or (cv2.waitKey(1) & 0xFF == 27):
            break

    cap.release()
    cv2.destroyAllWindows()