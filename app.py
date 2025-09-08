import tkinter as tk
import cv2
from PIL import Image, ImageTk
import face_recognition
import os
import pickle
import datetime
import numpy as np

import util
from test import test

class App:
    def __init__(self):
        self.main_window = tk.Tk()
        self.main_window.title("Face Recognition Attendance System")
        self.main_window.geometry("1200x520+350+100")

        # Buttons
        self.login_button_main_window = util.get_button(self.main_window, 'Login', 'green', self.login)
        self.login_button_main_window.place(x=750, y=200)

        self.logout_button_main_window = util.get_button(self.main_window, 'Logout', 'red', self.logout)
        self.logout_button_main_window.place(x=750, y=300)

        self.register_new_user_button_main_window = util.get_button(
            self.main_window, 'Register New User', 'gray',
            self.register_new_user, fg='black'
        )
        self.register_new_user_button_main_window.place(x=750, y=400)

        # Webcam
        self.webcam_label = util.get_img_label(self.main_window)
        self.webcam_label.place(x=10, y=0, width=700, height=500)
        self.add_webcam(self.webcam_label)

        # DB & log
        self.db_dir = './db'
        if not os.path.exists(self.db_dir):
            os.mkdir(self.db_dir)

        self.log_path = './log.txt'

    def add_webcam(self, label):
        if 'cap' not in self.__dict__:
            self.cap = cv2.VideoCapture(1)  # change index if needed
        self._label = label
        self.process_webcam()
    def process_webcam(self):
        ret, frame = self.cap.read()
        if not ret or frame is None:
            print("❌ Failed to grab frame from webcam")
            self._label.after(100, self.process_webcam)
            return

        self.most_recent_capture_arr = frame  # This is BGR uint8
        img_ = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert to RGB
        self.most_recent_capture_pil = Image.fromarray(img_)
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        self._label.imgtk = imgtk
        self._label.configure(image=imgtk)
        self._label.after(20, self.process_webcam)

   

    def login(self):
        label = test(self.most_recent_capture_arr)  # spoof detection

        if label == 1:  # real person
            name = util.recognize(self.most_recent_capture_arr, self.db_dir)

            if name is None or name in ['unknown_person', 'no_persons_found']:
                util.msg_box(
                    'Oops...',
                    'Unknown user! Please register a new user or try again.'
                )
            else:
                util.msg_box('Welcome Back!', f'Welcome, {name}.')
                with open(self.log_path, 'a') as f:
                    f.write(f'{name},{datetime.datetime.now()},in\n')
        else:
            util.msg_box('Alert!', 'You are a spoofer!')


    def logout(self):
        label = test(self.most_recent_capture_arr)  
        if label == 1:
            name = util.recognize(self.most_recent_capture_arr, self.db_dir)
            if name in ['unknown_person', 'no_persons_found']:
                util.msg_box('Oops...', 'Unknown user. Please register new user or try again.')
            else:
                util.msg_box('Goodbye!', f'Goodbye, {name}.')
                with open(self.log_path, 'a') as f:
                    f.write(f'{name},{datetime.datetime.now()},out\n')
        else:
            util.msg_box('Alert!', 'You are a spoofer!')

    def register_new_user(self):
        self.register_new_user_window = tk.Toplevel(self.main_window)
        self.register_new_user_window.title("Register New User")
        self.register_new_user_window.geometry("1200x520+370+120")

        self.accept_button_register_new_user_window = util.get_button(
            self.register_new_user_window, 'Accept', 'green', self.accept_register_new_user
        )
        self.accept_button_register_new_user_window.place(x=750, y=300)

        self.try_again_button_register_new_user_window = util.get_button(
            self.register_new_user_window, 'Try Again', 'red', self.try_again_register_new_user
        )
        self.try_again_button_register_new_user_window.place(x=750, y=400)

        self.capture_label = util.get_img_label(self.register_new_user_window)
        self.capture_label.place(x=10, y=0, width=700, height=500)
        self.add_img_to_label(self.capture_label)

        self.entry_text_register_new_user = util.get_entry_text(self.register_new_user_window)
        self.entry_text_register_new_user.place(x=750, y=150)

        self.text_label_register_new_user = util.get_text_label(
            self.register_new_user_window, 'Please input username:'
        )
        self.text_label_register_new_user.place(x=750, y=70)

    def try_again_register_new_user(self):
        self.register_new_user_window.destroy()

    def add_img_to_label(self, label):
        imgtk = ImageTk.PhotoImage(image=self.most_recent_capture_pil)
        label.imgtk = imgtk
        label.configure(image=imgtk)
        self.register_new_user_capture = self.most_recent_capture_arr.copy()

    def accept_register_new_user(self):
        name = self.entry_text_register_new_user.get(1.0, "end-1c").strip()
        img = self.register_new_user_capture
    
        if img is None:
            util.msg_box('Error', 'No image captured! Try again.')
            return
    
        if not isinstance(img, np.ndarray):
            img = np.array(img)
    
        if img.dtype != np.uint8:
            img = img.astype(np.uint8)
    
        if len(img.shape) == 2:  
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        elif img.shape[2] == 4: 
            img = cv2.cvtColor(img, cv2.COLOR_BGRA2RGB)
        else:  
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
        encodings = face_recognition.face_encodings(img)
        if len(encodings) == 0:
            util.msg_box('Error', 'No face found in the image. Try again!')
            return
    
        embeddings = encodings[0]
    
        file_path = os.path.join(self.db_dir, f'{name}.pickle')
        with open(file_path, 'wb') as f:
            pickle.dump(embeddings, f)
    
        util.msg_box('Success!', 'User was registered successfully!')
        self.register_new_user_window.destroy()
    

    def start(self):
        self.main_window.mainloop()


if __name__ == "__main__":
    app = App()
    app.start()
