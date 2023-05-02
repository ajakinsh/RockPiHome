import tkinter as tk
from datetime import datetime
import face_recognition
import cv2
import zmq
import imagezmq
import numpy as np

# Connect to Cam
image_receiver = imagezmq.ImageHub()


context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5558")

stream = True

class HomeownerPanel(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # Welcome label at top left corner
        welcome_label = tk.Label(self, text="WELCOME HOMEOWNER!", font=("Helvetica", 30, "bold"), pady=10, padx=10)
        welcome_label.grid(row=0, column=0, padx=10, pady=10, sticky='w')

        # Time display at top right corner
        self.time_label = tk.Label(self, text="", font=("Helvetica", 24) )
        self.time_label.grid(row=0, column=1, padx=10, pady=10, sticky='e')
        self.update_time()

        # Users Center section
        global users_frame
        users_frame = tk.LabelFrame(self, text="Users Center", font=("Helvetica", 14), padx=10, pady=10)
        users_frame.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        add_face_button = tk.Button(users_frame, text="Add Face ID", font=("Helvetica", 14), command=self.add_face)
        add_face_button.pack(side='top', pady=10)

        delete_face_button = tk.Button(users_frame, text="Delete Face ID", font=("Helvetica", 14), command=self.delete_face)
        delete_face_button.pack(side='top', pady=10)

        add_fingerprint_button = tk.Button(users_frame, text="Add Fingerprint", font=("Helvetica", 14), command=self.add_fingerprint)
        add_fingerprint_button.pack(side='top', pady=10)

        delete_fingerprint_button = tk.Button(users_frame, text="Delete Fingerprint", font=("Helvetica", 14), command=self.delete_fingerprint)
        delete_fingerprint_button.pack(side='top', pady=10)

        # Control Center section
        global control_frame
        control_frame = tk.LabelFrame(self, text="Control Center", font=("Helvetica", 14), padx=10, pady=10)
        control_frame.grid(row=1, column=1, padx=10, pady=10, sticky='nsew')

        # Video Control
        global stream_video_button
        stream_video_button = tk.Button(control_frame, text="Stream Video", font=("Helvetica", 14), command=self.stream_video)
        stream_video_button.pack(side='top', pady=10)

        # Lock Control
        self.locked = True
        self.lock_unlock_button = tk.Button(control_frame, text="PRESS TO UNLOCK", font=("Helvetica", 14), command=self.toggle_lock)
        self.lock_unlock_button.pack(side='top', pady=10)

        # System Status section
        global status_frame
        status_frame = tk.LabelFrame(self, text="System Status", font=("Helvetica", 14), padx=10, pady=10)
        status_frame.grid(row=5, column=0, padx=10, pady=10, sticky='nsew')

        global status_label
        # add a label widget inside the status_frame
        status_label = tk.Label(status_frame, text="Status: OK", font=("Helvetica", 14))
        status_label.pack()

    def update_time(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.configure(text=current_time)
        self.after(1000, self.update_time)

    def add_face(self):
        def add_face_id(face_id):
            # Code to send face_id and name to the RockPi
            success_lbl = tk.Label(popup, text=f"Added face ID: {face_id} to the database", font=("Helvetica", 12), fg="green")
            success_lbl.pack(pady=5)
            print(f"Adding face ID: {face_id} to the database")
            data = f"add_face: {face_id}"
            socket.send_multipart([b"add_face", data.encode()])
            success_lbl.after(2000, success_lbl.destroy)

        popup = tk.Toplevel(root)
        popup.geometry("1000x450")
        popup.title("Add Face ID")
        popup_lbl = tk.Label(popup, text="Stand in front of the camera. Press q to capture your Face ID image. Make sure your face is properly in the frame", font=("Helvetica", 12))
        popup_lbl.pack(padx=20, pady=10)

        id_label = tk.Label(popup, text="Enter a numerical ID for this face:", font=("Helvetica", 12))
        id_label.pack(pady=5)
        id_entry = tk.Entry(popup, font=("Helvetica", 12))
        id_entry.pack(pady=10)

        def add_id():
            face_id = id_entry.get()
            if face_id.isdigit():
                add_face_id(face_id)
            else:
                error_lbl = tk.Label(popup, text="Please enter a numerical ID", font=("Helvetica", 12), fg="red")
                error_lbl.after(2000, error_lbl.destroy)
                error_lbl.pack(pady=5)

        ok_btn = tk.Button(popup, text="OK", font=("Helvetica", 12), command=add_id)
        ok_btn.pack(padx=20, pady=10)

    def delete_face(self):
        def delete_face_id(face_id):
            success_lbl = tk.Label(popup, text=f"Deleted face ID: {face_id} ", font=("Helvetica", 12), fg="blue")
            success_lbl.pack(pady=5)
            print(f"Deleted face ID: {face_id} from the database")
            data = f"del_face: {face_id}"
            socket.send_multipart([b"del_face", data.encode()])
            success_lbl.after(2000, success_lbl.destroy)

        popup = tk.Toplevel(root)
        popup.geometry("500x200")
        popup.title("Delete Face ID")
        popup_lbl = tk.Label(popup, text="Enter the numerical ID of the face you want to delete", font=("Helvetica", 12))
        popup_lbl.pack(padx=20, pady=10)
        entry_label = tk.Label(popup, text="Face ID:", font=("Helvetica", 12))
        entry_label.pack(pady=5)
        entry = tk.Entry(popup, font=("Helvetica", 12))
        entry.pack(pady=10)

        def delete_id():
            face_id = entry.get()
            if face_id.isdigit():
                delete_face_id(face_id)
            else:
                error_lbl = tk.Label(popup, text="Please enter a numerical ID", font=("Helvetica", 12), fg="red")
                error_lbl.after(2000, error_lbl.destroy)
                error_lbl.pack(pady=5)

        ok_btn = tk.Button(popup, text="OK", font=("Helvetica", 12), command=delete_id)
        ok_btn.pack(padx=20, pady=10)

    def add_fingerprint(self):
        def add_finger_id(finger_id):
            success_lbl = tk.Label(popup, text=f"Added finger {finger_id}", font=("Helvetica", 12), fg="green")
            success_lbl.pack(pady=5)
            print(f"Adding finger ID: {finger_id} to the database")
            data = f"add_finger: {finger_id}"
            socket.send_multipart([b"add_finger", data.encode()])
            success_lbl.after(2000, success_lbl.destroy)

        popup = tk.Toplevel(root)
        popup.geometry("1000x250")
        popup.title("Add Finger ID")
        popup_lbl = tk.Label(popup, text="Place your finger on the sensor and wait for instructions", font=("Helvetica", 12))
        popup_lbl.pack(padx=20, pady=10)
        entry_label = tk.Label(popup, text="Fingerprint ID:", font=("Helvetica", 12))
        entry_label.pack(pady=5)
        entry = tk.Entry(popup, font=("Helvetica", 12))
        entry.pack(pady=10)

        def add_id():
            finger_id = entry.get()
            if finger_id.isdigit():
                add_finger_id(finger_id)
            else:
                error_lbl = tk.Label(popup, text="Please enter a numerical ID", font=("Helvetica", 12), fg="red")
                error_lbl.after(2000, error_lbl.destroy)
                error_lbl.pack(pady=5)

        ok_btn = tk.Button(popup, text="OK", font=("Helvetica", 12), command=add_id)
        ok_btn.pack(padx=20, pady=10)


    def delete_fingerprint(self):
        def delete_finger_id(finger_id):
            # Code to send face_id and name to the RockPi
            success_lbl = tk.Label(popup, text=f"Deleted finger {finger_id}", font=("Helvetica", 12), fg="blue")
            success_lbl.pack(pady=5)
            print(f"Deleting finger ID: {finger_id} from the database")
            data = f"del_finger: {finger_id}"
            socket.send_multipart([b"del_finger", data.encode()])
            success_lbl.after(2000, success_lbl.destroy)


        popup = tk.Toplevel(root)
        popup.geometry("500x200")
        popup.title("Delete Fingerprint ID")
        popup_lbl = tk.Label(popup, text="Enter the numerical ID of the fingerprint you want to delete", font=("Helvetica", 12))
        popup_lbl.pack(padx=20, pady=10)
        entry_label = tk.Label(popup, text="Fingerprint ID:", font=("Helvetica", 12))
        entry_label.pack(pady=5)
        entry = tk.Entry(popup, font=("Helvetica", 12))
        entry.pack(pady=10)

        def delete_id():
            finger_id = entry.get()
            if finger_id.isdigit():
                delete_finger_id(finger_id)
            else:
                error_lbl = tk.Label(popup, text="Please enter a numerical ID", font=("Helvetica", 12), fg="red")
                error_lbl.after(2000, error_lbl.destroy)
                error_lbl.pack(pady=5)

        ok_btn = tk.Button(popup, text="OK", font=("Helvetica", 12), command=delete_id)
        ok_btn.pack(padx=20, pady=10)


    def stream_video(self):
        # Code to stream video from camera

        # # Connect to Cam
        # image_receiver = imagezmq.ImageHub(bind_addr="tcp://*:5556")
        # context = zmq.Context()
        # msg_client = context.socket(zmq.REP)
        # # msg_client.connect("tcp://10.144.113.225:5556")
        # msg_client.connect("tcp://10.144.113.8:5556")
        # stream = True

        global stream

        while True:
            if stream:
                socket.send_multipart([b"stream", b"stream"])
                # Receive from the camera
                ret, frame = image_receiver.recv_image()
                small_frame = cv2.resize(frame, (384, 216)) # make image smaller if huge
                cv2.imshow("Video Stream", small_frame)
                # status_label = tk.Label(status_frame, text="Connected to camera", font=("Helvetica", 14))
                # status_label.pack()
                # cv2.waitKey(1)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    stream = False
            else:
                socket.send_multipart([b"stream", b"stopVid"])
                ret, frame = image_receiver.recv_image()
                image_receiver.send_reply(b'stream suspended')
                cv2.destroyAllWindows()

    def toggle_lock(self):
        self.locked = not self.locked
        lock_state = "locked" if self.locked else "unlocked"
        self.lock_unlock_button.config(text="PRESS TO UNLOCK" if self.locked else "PRESS TO LOCK")
        status_label.config(text=f'System Status: {lock_state}')
        # Send lock state to the server
        lock_state_msg = "locked" if self.locked else "unlocked"
        socket.send_multipart([b"locked", lock_state_msg.encode()])

def on_closing():
    global stream
    stream = False
    root.destroy()
    socket.close()
    # context.term()
    # context.destroy()
    image_receiver.close()
    print("closed")

if __name__ == '__main__':
    try:
        root = tk.Tk()
        root.title("Home Control Panel")
        root.geometry("1000x500")
        # Add some colors and shapes to the panel
        root.configure(bg="white")
        panel = HomeownerPanel(root)
        panel.pack(expand=True, fill='both')
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
    finally:
        on_closing()
