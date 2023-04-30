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
msg_client = context.socket(zmq.REP)
# msg_client.connect("tcp://10.144.113.8:5556")
msg_client.connect("tcp://10.144.113.90:5556")
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
        # Code to stream video from camera

        # create a new window for video stream
        video_window = tk.Toplevel(root)
        video_window.title("Video Stream")

        # create a canvas to display the video stream
        canvas = tk.Canvas(video_window, width=640, height=480)
        canvas.pack()

        # # Connect to Cam
        # image_receiver = imagezmq.ImageHub(bind_addr="tcp://*:5556")
        # context = zmq.Context()
        # msg_client = context.socket(zmq.REP)
        # # msg_client.connect("tcp://10.144.113.225:5556")
        # msg_client.connect("tcp://10.144.113.8:5556")
        # stream = True

        # Load the reference image
        reference_image = face_recognition.load_image_file("jess.jpg")
        reference_encoding = face_recognition.face_encodings(reference_image)[0]

        global stream 
        if stream:
            msg_client.send(b'stream')
            # Receive from the camera
            ret, frame = image_receiver.recv_image()
            small_frame = cv2.resize(frame, (384, 216)) # make image smaller if huge
            cv2.imshow("Video Stream", small_frame)
            # cv2.waitKey(1) 
            if cv2.waitKey(1) & 0xFF == ord('q'):
                stream = False

            else:
                msg_client.send(b'stopVid')
                ret, frame = image_receiver.recv_image()
                image_receiver.send_reply(b'stream suspended')
                cv2.destroyAllWindows()

        # Wait for the camera to warm up
        while True:
            
            # Convert the image to RGB format
            rgb_image = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

            # Detect faces in the image
            face_locations = face_recognition.face_locations(rgb_image)
            face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

            # Draw a box around each detected face
            for top, right, bottom, left in face_locations:
                cv2.rectangle(small_frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Compare each detected face to the reference image
            for face_encoding in face_encodings:
                match = face_recognition.compare_faces([reference_encoding], face_encoding, tolerance = 0.6)
                if match[0]:
                    print("Found Jess!")
                    # Draw a green box around the matched face
                    cv2.rectangle(small_frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(small_frame, "Hi Jess", (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Display the resulting image
            cv2.imshow('Video', small_frame)

            # Wait for a key press
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Release the camera and close the window
        cv2.destroyAllWindows()

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