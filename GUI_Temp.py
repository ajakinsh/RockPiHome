import tkinter as tk
from datetime import datetime

class HomeownerPanel(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # Welcome label at top left corner
        welcome_label = tk.Label(self, text="WELCOME HOMEOWNER!")
        welcome_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        # Time display at top right corner
        self.time_label = tk.Label(self, text="")
        self.time_label.grid(row=0, column=1, padx=10, pady=10, sticky='e')
        self.update_time()

        # Users Center section
        global users_frame
        users_frame = tk.LabelFrame(self, text="Users Center", padx=10, pady=10)
        users_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        add_face_button = tk.Button(users_frame, text="Add Face ID", command=self.add_face_popup)
        add_face_button.pack(side='top', pady=10)

        delete_face_button = tk.Button(users_frame, text="Delete Face ID", command=self.delete_face)
        delete_face_button.pack(side='top', pady=10)

        add_fingerprint_button = tk.Button(users_frame, text="Add Fingerprint", command=self.fingerprint_id_popup)
        add_fingerprint_button.pack(side='top', pady=10)

        delete_fingerprint_button = tk.Button(users_frame, text="Delete Fingerprint", command=self.delete_fingerprint)
        delete_fingerprint_button.pack(side='top', pady=10)

        # Control Center section
        global control_frame
        control_frame = tk.LabelFrame(self, text="Control Center", padx=10, pady=10)
        control_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

        stream_video_button = tk.Button(control_frame, text="Stream Video", command=self.stream_video)
        stream_video_button.pack(side='top', pady=10)

        lock_unlock_button = tk.Button(control_frame, text="Lock/Unlock Door", command=self.toggle_lock)
        lock_unlock_button.pack(side='top', pady=10)

        # Status label at top bottom
        system_status = tk.Label(self, text="System Status")
        system_status.grid(row=5, column=0, padx=10, pady=10, sticky='w')

        # System Status section
        system_status = tk.Label(self, text="System Status")
        system_status.grid(row=5, column=0, padx=10, pady=10, sticky='w')
        status_frame = tk.LabelFrame(self, text="Status", padx=10, pady=10)
        status_frame.grid(row=6, column=0, padx=10, pady=10, sticky='nsew')


    def update_time(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.configure(text=current_time)
        self.after(1000, self.update_time)

    # def popupmsg(msg):
    #     popup = Toplevel()
    #     popup.geometry('200x100')
    #     popup.title('Message')
    #     Label(popup, text=msg, font=('Verdana', 12)).pack(pady=10)
    #     Button(popup, text='OK', command=popup.destroy).pack()

    def add_face_popup(self):
        popup = tk.Toplevel(root)
        popup.geometry("300x100")
        popup.title("Add Face ID")
        popup_lbl = tk.Label(popup, text="Stand in front of the camera. Press q to capture your Face ID image. Make sure your face is properly in the frame", font=("Helvetica", 12))
        popup_lbl.pack(padx=20, pady=20)
        ok_btn = tk.Button(popup, text="OK", font=("Helvetica", 12), command=popup.destroy)
        ok_btn.pack(padx=20, pady=10)

    def fingerprint_id_popup(self):
        popup = tk.Toplevel(root)
        popup.geometry("300x100")
        popup.title("Add Face ID")
        popup_lbl = tk.Label(popup, text="Place your finger on the sensor and wait for instructions", font=("Helvetica", 12))
        popup_lbl.pack(padx=20, pady=20)
        ok_btn = tk.Button(popup, text="OK", font=("Helvetica", 12), command=popup.destroy)
        ok_btn.pack(padx=20, pady=10)

    # def add_face(self):
    #     # Code to add a face ID
    #     popupmsg("Stand in front of the camera. Press 'q' to capture your Face ID image. Make sure your face is properly in the frame.")
    #     pass

    def delete_face(self):
        # Code to delete a face ID
        pass

    # def add_fingerprint(self):
    #     # Code to add a fingerprint
    #     pass

    def delete_fingerprint(self):
        # Code to delete a fingerprint
        pass

    def stream_video(self):
        # Code to stream video from camera
        pass

    # def lock_unlock_door(self):
    #     # Code to lock or unlock the door
    #     pass

    def toggle_lock(self):
        if lock_unlock_button.config('text')[-1] == 'LOCK':
            lock_unlock_button.config(text='UNLOCK', bg='green')
        else:
            lock_unlock_button.config(text='LOCK', bg='red')

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Homeowner Panel")
    root.geometry("600x400")
    # Add some colors and shapes to the panel
    root.configure(bg="white")
    panel = HomeownerPanel(root)
    panel.pack(expand=True, fill='both')
    root.mainloop()