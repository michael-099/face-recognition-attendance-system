import tkinter as tk
from tkinter import messagebox
import cv2
import face_recognition
import os
import pickle

def get_button(window, text, color, command, fg='white'):
    return tk.Button(window, text=text, bg=color, fg=fg, command=command,
                     font=("Arial", 14), width=20, height=2)


def get_img_label(window):
    return tk.Label(window)


def get_entry_text(window):
    return tk.Text(window, height=1, width=20, font=("Arial", 14))


def get_text_label(window, text):
    return tk.Label(window, text=text, font=("Arial", 14))


def msg_box(title, message):
    messagebox.showinfo(title, message)


def recognize(img, db_path, tolerance=0.5):
    """
    Recognize a face from an image against stored encodings.

    Parameters
    ----------
    img : numpy.ndarray
        The captured image (BGR from OpenCV).
    db_path : str
        Path to the database folder containing .pickle encodings.
    tolerance : float
        How strict the face comparison is (default=0.5, lower = stricter).

    Returns
    -------
    str or None
        The recognized user's name, or None if no match is found.
    """
    # Convert BGR -> RGB (face_recognition expects RGB)
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Get encodings for the face(s) in the image
    encodings = face_recognition.face_encodings(rgb_img)
    if len(encodings) == 0:
        return None   # No face detected

    encoding = encodings[0]

    # Loop through all known encodings in db_path
    for file in os.listdir(db_path):
        if not file.endswith(".pickle"):
            continue

        filepath = os.path.join(db_path, file)
        with open(filepath, "rb") as f:
            known_encoding = pickle.load(f)

        # Compare current face to known encoding
        results = face_recognition.compare_faces([known_encoding], encoding, tolerance=tolerance)
        if results[0]:
            # Return the filename (without .pickle) as the user’s name
            return os.path.splitext(file)[0]

    # If no match found
    return None



