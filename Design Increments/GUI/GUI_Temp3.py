from datetime import datetime
import tkinter as tk
import face_recognition
import imagezmq
import zmq
import cv2

# # Set up socket for streaming video
# context = zmq.Context()
# footage_socket = context.socket(zmq.PUB)
# footage_socket.connect("tcp://<10.144.113.8>:5555")

# def stream_video():
#     cap = cv2.VideoCapture(0)

#     # Set video format to MJPG, required by imagezmq
#     cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc(*"MJPG"))

# Connect to Cam
image_receiver = imagezmq.ImageHub(bind_addr="tcp://*:5556")
context = zmq.Context()
msg_client = context.socket(zmq.REP)
msg_client.connect("tcp://10.144.113.8:5556")
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
        global lock_unlock_button
        lock_unlock_button = tk.Button(control_frame, text="Lock/Unlock Door", font=("Helvetica", 14), command=self.toggle_lock)
        lock_unlock_button.pack(side='top', pady=10)

        # System Status section
        global status_frame
        status_frame = tk.LabelFrame(self, text="System Status", font=("Helvetica", 14), padx=10, pady=10)        
        status_frame.grid(row=5, column=0, padx=10, pady=10, sticky='nsew')

        # add a label widget inside the status_frame
        status_label = tk.Label(status_frame, text="Status: OK", font=("Helvetica", 14),)
        status_label.pack()

    def update_time(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.configure(text=current_time)
        self.after(1000, self.update_time)

    def add_face(self):
        popup = tk.Toplevel(root)
        popup.geometry("1000x200")
        popup.title("Add Face ID")
        popup_lbl = tk.Label(popup, text="Stand in front of the camera. Press q to capture your Face ID image. Make sure your face is properly in the frame", font=("Helvetica", 12))
        popup_lbl.pack(padx=20, pady=20)
        ok_btn = tk.Button(popup, text="OK", font=("Helvetica", 12), command=popup.destroy)
        ok_btn.pack(padx=20, pady=10)
    
    def delete_face(self):
        # Code to delete a face ID
        pass

    def add_fingerprint(self):
        popup = tk.Toplevel(root)
        popup.geometry("1000x200")
        popup.title("Add Face ID")
        popup_lbl = tk.Label(popup, text="Place your finger on the sensor and wait for instructions", font=("Helvetica", 12))
        popup_lbl.pack(padx=20, pady=20)
        ok_btn = tk.Button(popup, text="OK", font=("Helvetica", 12), command=popup.destroy)
        ok_btn.pack(padx=20, pady=10)

    def delete_fingerprint(self):
        # Code to delete a fingerprint
        pass

    def stream_video(self):
        # Code to stream video from camera
        pass

    def toggle_lock(self):
        # Code to lock or unlock the door
        if lock_unlock_button.config('text')[-1] == 'LOCK':
            lock_unlock_button.config(text='UNLOCK', bg='green')
        else:
            lock_unlock_button.config(text='LOCK', bg='red')

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Home Control Panel")
    root.geometry("1000x500")
    # Add some colors and shapes to the panel
    root.configure(bg="white")
    panel = HomeownerPanel(root)
    panel.pack(expand=True, fill='both')
    root.mainloop()





#     while True:
#         # Read frame from camera
#         ret, frame = cap.read()

#         # Send frame to socket
#         footage_socket.send(cv2.imencode(".jpg", frame)[1])

#         # Display frame in GUI
#         cv2.imshow("Stream", frame)

#         # Break loop if user presses 'q'
#         if cv2.waitKey(1) == ord("q"):
#             break

#     # Release video capture and destroy window
#     cap.release()
#     cv2.destroyAllWindows()