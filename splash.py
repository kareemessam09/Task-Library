from tkinter import *
from tkinter import ttk
import os

import sys
import subprocess

def call_main_app():
    # Destroy the splash screen
    splash.destroy()
    # Launch the main login application using subprocess
    subprocess.Popen([sys.executable, "login_register.py"])

# Create Splash Screen Window
splash = Tk()
splash.title("Splash Screen")
splash.geometry("500x300")

# Remove title bar
splash.overrideredirect(True)

# Center the splash screen on the monitor
screen_width = splash.winfo_screenwidth()
screen_height = splash.winfo_screenheight()
x = (screen_width / 2) - (500 / 2)
y = (screen_height / 2) - (300 / 2)
splash.geometry(f'500x300+{int(x)}+{int(y)}')

splash.config(bg='Orange')

# Add Labels
title_label = Label(splash, text="Library Management System", font=('Georgia', 24, 'bold'), bg='Orange')
title_label.pack(pady=70)

loading_label = Label(splash, text="Loading...", font=('Arial', 14, 'italic'), bg='Orange')
loading_label.pack(pady=5)

# Add Progress Bar
progress = ttk.Progressbar(splash, orient=HORIZONTAL, length=300, mode='determinate')
progress.pack(pady=10)

def load_animation():
    # Simulate loading progress
    for i in range(1, 101):
        progress['value'] = i
        splash.update_idletasks()
        splash.after(20)  # Wait 20ms between updates
    
    # Wait half a second after filling, then open the main app
    splash.after(500, call_main_app)

# Start the loading animation slightly after the window appears
splash.after(200, load_animation)

splash.mainloop()
