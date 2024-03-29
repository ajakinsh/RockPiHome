import tkinter as tk
import cv2
import serial as ser
import cv2
import os

cmd_add = 'ssh rock@10.144.113.116 "python add_face.py face.jpg"'
cmd_delete = 'ssh rock@10.144.113.116 "python delete_face.py"'

# Configure serial communication with Arduino Teensy
#ser = serial.Serial('/dev/ttyACM0', 9600)

# Open video capture device
cap = cv2.VideoCapture(0)

# Create a Tkinter Frame
root = tk.Tk()
root.geometry("600x400")
root.title("Home Security Control Panel")


# Streaming Video Function
def stream_video():
    # code for streaming video from the camera
    # add CODE here
    x=9

# Fingerprint Functions

# Define function for adding fingerprint ID
def add_fingerprint():
    # Send command to Arduino Teensy to add fingerprint
    ser.write(b'add_fingerprint')

    # Wait for response from Arduino Teensy
    response = ser.readline().decode().strip()

    if response == 'Fingerprint added successfully':
        print('Fingerprint added successfully')
    else:
        print('Error: ' + response)

# Define function for deleting fingerprint ID
def delete_fingerprint():
    # Send command to Arduino Teensy to delete fingerprint
    ser.write(b'delete_fingerprint')

    # Wait for response from Arduino Teensy
    response = ser.readline().decode().strip()

    if response == 'Fingerprint deleted successfully':
        print('Fingerprint deleted successfully')
    else:
        print('Error: ' + response)



# Face ID Functions


# Define function for adding face ID
def add_face():
    # Capture an image from the camera
    ret, img = cap.read()

    # Save the image to file
    cv2.imwrite('face.jpg', img)

    # Send command to Rock Pi to add face ID
    # Replace IP address with the IP address of your Rock Pi
    #os.system('ssh root@192.168.1.100 "python add_face.py face.jpg"')
    os.system(cmd_add)

# Define function for deleting face ID
def delete_face():
    # Send command to Rock Pi to delete face ID
    # Replace IP address with the IP address of your Rock Pi
    os.system(cmd_delete)

# Create Buttons for each functionality
stream_button = tk.Button(root, text="Stream Video", command=stream_video)
add_fingerprint_button = tk.Button(root, text="Add Fingerprint", command=add_fingerprint)
delete_fingerprint_button = tk.Button(root, text="Delete Fingerprint", command=delete_fingerprint)
add_face_button = tk.Button(root, text="Add Face ID", command=add_face)
delete_face_button = tk.Button(root, text="Delete Face ID", command=delete_face)

# Place Buttons in Tkinter Window
stream_button.pack()
add_fingerprint_button.pack()
delete_fingerprint_button.pack()
add_face_button.pack()
delete_face_button.pack()

#Run the GUI
root.mainloop()