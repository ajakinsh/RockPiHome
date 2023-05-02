import tkinter as tk
from tkinter import ttk
import time

class HomeownerPanel(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Homeowner Panel")
        self.geometry("800x600")
        self.configure(bg="#FFFFFF")
        self.resizable(False, False)

        # Add a label at the top left corner saying "WELCOME HOMEOWNER!"
        welcome_label = tk.Label(self, text="WELCOME HOMEOWNER!", font=("Helvetica", 24), fg="#000000", bg="#FFFFFF")
        welcome_label.grid(row=0, column=0, padx=20, pady=20, sticky="w")

        # Add a time display at the top right corner
        self.time_label = tk.Label(self, text="", font=("Helvetica", 18), fg="#000000", bg="#FFFFFF")
        self.time_label.grid(row=0, column=1, padx=20, pady=20, sticky="e")
        self.update_time()

        # Section on the left side of the panel called "Users Center"
        users_center_frame = tk.Frame(self, bg="#FFFFFF", highlightbackground="#000000", highlightthickness=2)
        users_center_frame.grid(row=1, column=0, padx=20, pady=20, sticky="nsew")

        users_center_label = tk.Label(users_center_frame, text="Users Center", font=("Helvetica", 18), fg="#000000", bg="#FFFFFF")
        users_center_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Add buttons for adding and deleting face ID or fingerprint
        add_face_id_button = tk.Button(users_center_frame, text="Add Face ID", font=("Helvetica", 14), bg="#FFFFFF", command=self.add_face_id)
        add_face_id_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")

       delete_face_id_button = tk.Button(users_center_frame, text="Delete Face ID", font=("Helvetica", 14), bg="#FFFFFF", command=self.delete_face_id)
        delete_face_id_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")

        # A different section on the right side of the panel called "Control Center"
        control_center_frame = tk.Frame(self, bg="#FFFFFF", highlightbackground="#000000", highlightthickness=2)
        control_center_frame.grid(row=1, column=1, padx=20, pady=20, sticky="nsew")

        control_center_label = tk.Label(control_center_frame, text="Control Center", font=("Helvetica", 18), fg="#000000", bg="#FFFFFF")
        control_center_label.grid(row=0, column=0, padx=10, pady=10, sticky="w")

        # Add buttons for streaming video and locking/unlocking door
        stream_video_button = ttk.Checkbutton(control_center_frame, text="Stream Video", font=("Helvetica", 14), cursor="hand2")
        stream_video_button.grid(row=1, column=0, padx=10, pady=10, sticky="w")

        lock_unlock_button = ttk.Checkbutton(control_center_frame, text="Lock/Unlock Door", font=("Helvetica", 14), cursor="hand2")
        lock_unlock_button.grid(row=2, column=0, padx=10, pady=10, sticky="w")
