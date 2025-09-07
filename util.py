import tkinter as tk
from tkinter import messagebox

def get_ing_label(window):
    label = tk.Label(window)
    label.grid(row=0, column=0)
    return label

def get_text_label(window, text):
    label = tk.Label(window, text=text)
    label.config(font=("sans-serif", 21), justify="left")
    return label

def get_entry_text(window):
    inpuT_txt = tk.Text(window, height=2, width=15, font=("Arial", 32))
    return inpuT_txt

def msg_box(title, description):
    messagebox.showinfo(title, description)
    return

def get_button(text, color, command, window):
    canvas = tk.Canvas(window, width=200, height=50, bg="black", highlightthickness=0)
    canvas.grid(row=1, column=0) 

    radius = 25  
    canvas.create_rounded_rectangle(10, 10, 190, 40, radius=radius, fill=color, outline="white")

    canvas.create_text(100, 25, text=text, fill="white", font=("Helvetica bold", 20))

    def on_click(event):
        command()

    canvas.bind("<Button-1>", on_click)
    return canvas
  

