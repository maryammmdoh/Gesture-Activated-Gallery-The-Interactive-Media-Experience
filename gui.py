import tkinter as tk
from tkinter import ttk
import cv2
import mediapipe as mp
import numpy as np
from threading import Thread
import socket

# MediaPipe setup
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

def send_gesture_to_csharp(gesture):
    HOST, PORT = "localhost", 9999
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        sock.sendall(bytes(gesture, "utf-8"))

# This function is used to detect hand gestures and interact with the GUI
def detect_gestures():
    # Start the webcam
    cap = cv2.VideoCapture(0)

    while cap.isOpened():
        success, image = cap.read()
        if not success:
            continue

        # Flip the image horizontally for a later selfie-view display
        # And convert the BGR image to RGB.
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        # Process the image and find hands
        results = hands.process(image)

        # Draw hand landmarks
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Here you can check for gestures and trigger actions on the GUI
                
                # Example: Check if the index finger is up and simulate a button click
                if hand_is_clicking(hand_landmarks):
                    # Simulate button click or any other GUI interaction
                    pass

        # You can add here other logic to communicate with your C# application via sockets

        # If you want to display the image with annotations (for debugging)
        # cv2.imshow('MediaPipe Hands', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break

    cap.release()

# Dummy function to check if a hand is clicking
def hand_is_clicking(hand_landmarks):
    # You would add logic here to determine if a gesture is being made
    return False

# Start the hand gesture detection in a separate thread
thread = Thread(target=detect_gestures)
thread.daemon = True
thread.start()

# Initialize main application window
root = tk.Tk()
root.title("Interactive Magazine")
root.geometry("800x600")  # Set the window size

# Set attractive colors and fonts
bg_color = "#FFE5B4"  # A light pastel background
button_color = "#FF7F50"  # Coral-like color for buttons
text_font = ("Arial", 12)
heading_font = ("Arial", 18, "bold")

# Configure the grid layout
root.columnconfigure(0, weight=1)
root.columnconfigure(1, weight=4)
root.rowconfigure(0, weight=1)

# Define functions for interactivity
def show_article(content):
    # Function to update the reading pane with the content of the clicked article
    text_area.config(state=tk.NORMAL)
    text_area.delete(1.0, tk.END)
    text_area.insert(tk.END, content)
    text_area.config(state=tk.DISABLED)

def enter_application():
    welcome_frame.grid_forget()  # Hide the welcome page
    main_frame.grid(row=0, column=0, sticky="nsew", columnspan=2)  # Show the main content
    nav_pane.grid(row=0, column=0, sticky="ns")
    reading_pane.grid(row=0, column=1, sticky="nsew")

def close_on_esc(event):
    root.destroy()

root.bind('<Escape>', close_on_esc)

# Main content frame, which we will show later
main_frame = tk.Frame(root)
main_frame.grid(row=0, column=0, sticky="nsew", columnspan=2)
main_frame.columnconfigure(0, weight=1)
main_frame.columnconfigure(1, weight=4)
main_frame.rowconfigure(0, weight=1)

# Welcome page frame
welcome_frame = tk.Frame(root, bg=bg_color)
welcome_frame.grid(row=0, column=0, sticky="nsew", columnspan=2)

# Welcome message and button
welcome_message = tk.Label(welcome_frame, text="Welcome to the Interactive Magazine!", font=heading_font, bg=bg_color)
welcome_message.pack(pady=50)
enter_button = tk.Button(welcome_frame, text="Enter", command=enter_application, font=text_font, padx=20, pady=10)
enter_button.pack()

# Hide main content initially
main_frame.grid_forget()

# Navigation pane
nav_pane = tk.Frame(main_frame, bg=bg_color)
# Don't grid it yet, will be done in enter_application()

# Reading pane
reading_pane = tk.Frame(main_frame, bg="white", padx=10, pady=10)
# Don't grid it yet, will be done in enter_application()

# Scrollbar for reading pane
scrollbar = ttk.Scrollbar(reading_pane)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Text widget for reading pane
text_area = tk.Text(reading_pane, yscrollcommand=scrollbar.set, font=text_font, state=tk.DISABLED, wrap=tk.WORD)
text_area.pack(expand=True, fill="both")
scrollbar.config(command=text_area.yview)

# Populate navigation pane with buttons
sections = ["Home", "Latest News", "Feature Articles", "Interviews", "Opinions", "Videos", "Quizzes"]
for section in sections:
    button = tk.Button(nav_pane, text=section, command=lambda sec=section: show_article(f"Content of {sec}"),
                       bg=button_color, fg="white", font=text_font, relief=tk.FLAT, padx=20, pady=10)
    button.pack(fill=tk.X, pady=5)

# Run the application
root.mainloop()