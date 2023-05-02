import zmq
import cv2
import imagezmq
import mraa
import time
import face_recognition
from datetime import datetime, timedelta
import serial
import threading
import signal
import os

GLOBAL_SER = "finger lock"
GLOBAL_KEY = "keypad lock"
GLOBAL_FACE = "face lock"
GLOBAL_FINGER = "check"

# set initial time
last_command_time = datetime.now()

# Define the possible serial port names
port1 = '/dev/ttyACM0'
port2 = '/dev/ttyACM1'
baudrate = 57600

try:
    ser = serial.Serial(port1, baudrate)
    print("Connected to", port1)
except:
    try:
        ser = serial.Serial(port2, baudrate)
        print("Connected to", port2)
    except:
        # If both ports fail, print an error message and exit
        print("Error: Could not connect to serial port")
        exit()

video_capture = cv2.VideoCapture(4)

image_sender = imagezmq.ImageSender('tcp://10.144.113.8:5555')

#context = zmq.Context()
#msg_server = context.socket(zmq.REP)
#msg_server.setsockopt(zmq.LINGER, 0)
#msg_server.bind('tcp://*:5557')

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect('tcp://10.144.113.8:5558')
socket.setsockopt(zmq.SUBSCRIBE, b"locked")
socket.setsockopt(zmq.SUBSCRIBE, b"stream")
socket.setsockopt(zmq.SUBSCRIBE, b"add_finger")
socket.setsockopt(zmq.SUBSCRIBE, b"del_finger")
socket.setsockopt(zmq.SUBSCRIBE, b"add_face")
socket.setsockopt(zmq.SUBSCRIBE, b"del_face")

# Saved Door Lock Code
saved_code = "5678"

# Initialize the typed code variable
typed_code = ""

LCD_CLEAR_DISPLAY = 0x01
LCD_RETURN_HOME = 0x02
LCD_TURN_OFF_CURSOR = 0x0C
LCD_SET_ENTRY_MODE = 0x06
LCD_LINE_2 = 0xC2

#Define LCD pins
lcd_rs = mraa.Gpio(16)
lcd_en = mraa.Gpio(18)
lcd_d0 = mraa.Gpio(13)
lcd_d1 = mraa.Gpio(15)
lcd_d2 = mraa.Gpio(19)
lcd_d3 = mraa.Gpio(21)
lcd_d4 = mraa.Gpio(23)
lcd_d5 = mraa.Gpio(22)
lcd_d6 = mraa.Gpio(24)
lcd_d7 = mraa.Gpio(32)
#cathode_pin = mraa.Gpio(8)
#anode_pin = mraa.Gpio(10)

# Set LCD pin directions
lcd_rs.dir(mraa.DIR_OUT)
lcd_en.dir(mraa.DIR_OUT)
lcd_d0.dir(mraa.DIR_OUT)
lcd_d1.dir(mraa.DIR_OUT)
lcd_d2.dir(mraa.DIR_OUT)
lcd_d3.dir(mraa.DIR_OUT)
lcd_d4.dir(mraa.DIR_OUT)
lcd_d5.dir(mraa.DIR_OUT)
lcd_d6.dir(mraa.DIR_OUT)
lcd_d7.dir(mraa.DIR_OUT)
#cathode_pin.dir(mraa.DIR_OUT)
#anode_pin.dir(mraa.DIR_OUT)

lcd_columns = 16
lcd_rows = 2

# Define LEDs
green = mraa.Gpio(3)
green.dir(mraa.DIR_OUT)
red = mraa.Gpio(12)
red.dir(mraa.DIR_OUT)

# Define Keypad rows
row1 = mraa.Gpio(29)
row1.dir(mraa.DIR_OUT)
row2 = mraa.Gpio(31)
row2.dir(mraa.DIR_OUT)
row3 = mraa.Gpio(33)
row3.dir(mraa.DIR_OUT)
row4 = mraa.Gpio(35)
row4.dir(mraa.DIR_OUT)

# Define Keypad columns
col1 = mraa.Gpio(37)
col1.dir(mraa.DIR_IN)
col2 = mraa.Gpio(36)
col2.dir(mraa.DIR_IN)
col3 = mraa.Gpio(38)
col3.dir(mraa.DIR_IN)
col4 = mraa.Gpio(40)
col4.dir(mraa.DIR_IN)

# Initialize LCD
def lcd_init():
    time.sleep(0.4)
    lcd_send_command(0x30)
    time.sleep(0.39)
    lcd_send_command(0x38)
    time.sleep(0.37)
    lcd_send_command(0x10)
    time.sleep(0.37)
    lcd_send_command(LCD_TURN_OFF_CURSOR)
    time.sleep(0.153)
    lcd_send_command(LCD_SET_ENTRY_MODE)
    time.sleep(0.4)
    lcd_send_command(LCD_RETURN_HOME)
    time.sleep(0.4)
    lcd_send_command(LCD_CLEAR_DISPLAY)
    time.sleep(0.4)

    lcd_en.write(1); lcd_rs.write(1);
    lcd_d0.write(0); lcd_d1.write(0); lcd_d2.write(0); lcd_d3.write(0);
    lcd_d4.write(0); lcd_d5.write(0); lcd_d6.write(0); lcd_d7.write(0);

def lcd_toggle_enable():
    lcd_en.write(1)
    time.sleep(0.05)
    lcd_en.write(0)
    time.sleep(0.05)

def lcd_send_eight_bits(data):
    lcd_d0.write(data & 0x01)
    lcd_d1.write((data >> 1) & 0x01)
    lcd_d2.write((data >> 2) & 0x01)
    lcd_d3.write((data >> 3) & 0x01)
    lcd_d4.write((data >> 4) & 0x01)
    lcd_d5.write((data >> 5) & 0x01)
    lcd_d6.write((data >> 6) & 0x01)
    lcd_d7.write((data >> 7) & 0x01)
    lcd_toggle_enable()

def lcd_send_command(command):
    lcd_rs.write(0)
    time.sleep(0.0039)
    lcd_send_eight_bits(command)
    lcd_toggle_enable()

def lcd_send_character(char):
    lcd_rs.write(1)
    lcd_send_eight_bits(ord(char))

def lcd_message(message):
    for char in message:
        lcd_send_character(char)

# Keypad Read
def read_keypad():
    # row 1
    row1.write(0)
    if col1.read() == 0:
        print("Button pressed: 1")
        # Add a small delay to debounce the button
        time.sleep(0.6)
        return('1')

    if col2.read() == 0:
        print("Button pressed: 2")
        time.sleep(0.6)
        return('2')

    if col3.read() == 0:
        print("Button pressed: 3")
        time.sleep(0.6)
        return('3')

    if col4.read() == 0:
        print("Button pressed: A")
        time.sleep(0.6)
        return('A')

    row1.write(1)

    #row 2
    row2.write(0)
    if col1.read() == 0:
        print("Button pressed: 4")
        time.sleep(0.6)
        return('4')

    if col2.read() == 0:
        print("Button pressed: 5")
        time.sleep(0.6)
        return('5')

    if col3.read() == 0:
        print("Button pressed: 6")
        time.sleep(0.6)
        return('6')

    if col4.read() == 0:
        print("Button pressed: B")
        time.sleep(0.6)
        return('B')

    row2.write(1)

    #row 3
    row3.write(0)
    if col1.read() == 0:
        print("Button pressed: 7")
        time.sleep(0.6)
        return('7')

    if col2.read() == 0:
        print("Button pressed: 8")
        time.sleep(0.6)
        return('8')

    if col3.read() == 0:
        print("Button pressed: 9")
        time.sleep(0.6)
        return('9')

    if col4.read() == 0:
        print("Button pressed: C")
        time.sleep(0.6)
        return('C')

    row3.write(1)

    #row 4
    row4.write(0)
    if col1.read() == 0:
        print("Button pressed: *")
        time.sleep(0.6)
        return('*')

    if col2.read() == 0:
        print("Button pressed: 0")
        time.sleep(0.6)
        return('0')

    if col3.read() == 0:
        print("Button pressed: #")
        time.sleep(0.6)
        return('#')

    if col4.read() == 0:
        print("Button pressed: D")
        time.sleep(0.6)
        return('D')

    row4.write(1)

def flash_red():
    red.write(1)
    green.write(0)
    time.sleep(0.3)
    red.write(0)
    time.sleep(0.3)
    red.write(1)
    time.sleep(0.3)
    red.write(0)
    time.sleep(0.3)
    red.write(1)


def serial_thread_func():
    global last_command_time
    global GLOBAL_FINGER
    global GLOBAL_SER
    while True:
        if ser.in_waiting > 0:
            # read from serial port
            ser_data = ser.readline().decode().rstrip()
            print("(Serial)\t", ser_data)

            # Check if message indicates a fingerprint match; update LCD
            if "Found ID #" in ser_data:
                GLOBAL_SER = "finger unlock"

            if "Did not find a match" in ser_data:
                GLOBAL_SER = "finger wrong"


        if GLOBAL_FINGER == "check":
            # check if it's time to send the command
            if datetime.now() - last_command_time >= timedelta(seconds=1):  # send command every second
                ser.write("C\n".encode())
                last_command_time = datetime.now()

        else:
            ser.write(GLOBAL_FINGER.encode())
            GLOBAL_FINGER = "check"


def signal_handler(signal, frame):
    socket.close()
    ser.close()
    print("Caught Ctrl-C. Shutting down")
    exit()

def socket_thread_func():
    global GLOBAL_FACE
    global GLOBAL_KEY

    while True:
        known_face_encodings = []
        known_faces_names = []
        
        #        try:
        for filename in os.listdir('./faces'):
            if filename.endswith('.jpg'):
                image_path = os.path.join('./faces', filename)
                image = face_recognition.load_image_file(image_path)
                face_encodings = face_recognition.face_encodings(image)
                known_face_encodings.append(face_encodings)
                known_faces_names.append(os.path.splitext(filename)[0])

        # # Detect faces in the image
        # unknown_image = face_recognition.load_image_file("unknown.jpg")
        # face_locations = face_recognition.face_locations(unknown_image)
        # face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

        # Capture a frame from the camera
        ret, frame = video_capture.read()
        small_frame = cv2.resize(frame, (384, 216)) # make image smaller if huge

        # Convert the image to RGB format
        rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

        # Detect faces in the image
        # live_face_locations = face_recognition.face_locations(rgb_frame)
        live_face_encodings = face_recognition.face_encodings(rgb_frame)

        for i, live_face_encoding in enumerate(live_face_encodings):
            matches = face_recognition.compare_faces(known_face_encodings, live_face_encoding)
            name = "Unknown"
            if True in matches:
                match_index = matches.index(True)
                name = known_faces_names[match_index]
                print(f"Found {name}!")
                GLOBAL_FACE = "face unlock"
                
        jess_image = face_recognition.load_image_file("./faces/jess.jpg")
        jess_encoding = face_recognition.face_encodings(jess_image)[0]
        
        jess_match = face_recognition.compare_faces(jess_encoding, live_face_encoding, tolerance = 0.6)
        if jess_match:
            print("Found Jess!")
            GLOBAL_FACE = "face unlock"

        # Compare each detected face to the face encodings in the file
        # for face_encoding, face_name in zip(known_face_encodings, known_faces_names):
        #     match = face_recognition.compare_faces([face_encoding], live_face_encodings, tolerance = 0.6)
        #     if match[0]:
        #         print(f"Found {face_name}!")
        #         GLOBAL_FACE = "face unlock"

        topic, message = socket.recv_multipart()

        print(f"(GUI)\t{message}")

        if message == "b'stream":
            reply = image_sender.send_image('Image: ', small_frame)
        if message == "b'stopVid":
            video_capture.release()
            cv2.destroyAllWindows()
        if message == "b'locked":
            GLOBAL_KEY = "gui lock"
        if message == "b'unlocked":
            GLOBAL_KEY = "gui unlock"
        if message.startswith(b'add_face'):
            face_id = message.decode().split(":")[1]
            face_id.trim()
            # Wait for the camera to warm up
            while True:
                for i in range(10):
                    video_capture.grab()
                # Display the resulting image
                cv2.imshow('Video', small_frame)

                # Wait for a key press
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break

            # Release the camera and close the window
            video_capture.release()
            cv2.destroyAllWindows()

            # Convert the image to RGB format
            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Detect faces in the image
            face_locations = face_recognition.face_locations(rgb_image)

            # Draw a box around each detected face
            for top, right, bottom, left in face_locations:
                cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

            # Save the image as a JPEG file
            cv2.imwrite(f"./faces/{face_id}.jpg", small_frame)

        if message.startswith(b'del_face'):
            try:
                face_id = message.decode().split(":")[1]
                face_id.trim()
                print(f'./faces/{face_id}.jpg')
                os.remove(f'./faces/{face_id}.jpg')
            except FileNotFoundError:
                print(f"File not found")
            except Exception as e:
                print(f"{str(e)}")

            # GLOBAL_FACE = f"del: {face_id}"
        if message.startswith(b'add_finger'):
            finger_id = message.decode().split(":")[1]
            GLOBAL_FINGER = f"E{finger_id}\n"
        if message.startswith(b'del_finger'):
            finger_id = message.decode().split(":")[1]
            GLOBAL_FINGER = "D{finger_id}\n"

#        finally:
#            socket.close()
            #context.term()
            #msg_server.destroy()
            # print("TERMINATED 2")

def keypad_thread_func():
    global GLOBAL_KEY
    global typed_code
    while True:
        # Read From Keypad
        key = read_keypad()
        if key:
            GLOBAL_KEY = "keypad entry"
            typed_code += str(key)

        if len(typed_code) == 4:
            if typed_code == saved_code:
                GLOBAL_KEY = "keypad unlock"
                print("Correct code")
                typed_code = ""
            else:
                GLOBAL_KEY = "keypad wrong"
                print("Incorrect code")
                typed_code = ""

def LCD_thread_func():
    global GLOBAL_SER
    global GLOBAL_KEY
    global GLOBAL_FACE
    global typed_code
    while True:
        # Get the current time and format it as a string
        current_time = datetime.now().strftime('%H:%M:%S')

        # Write the current time to the top line of the LCD
        lcd_send_command(LCD_RETURN_HOME)
        lcd_send_command(LCD_TURN_OFF_CURSOR)
        lcd_send_command(LCD_SET_ENTRY_MODE)
        lcd_message(current_time + "    ")

        # red led on
        red.write(1)
        green.write(0)

        if GLOBAL_SER == "finger unlock" or GLOBAL_FACE == "face unlock":
            lcd_send_command(LCD_RETURN_HOME)
            lcd_send_command(LCD_TURN_OFF_CURSOR)
            lcd_send_command(LCD_SET_ENTRY_MODE)

            # Write a message to the bottom line of the LCD
            lcd_send_command(LCD_LINE_2)
            lcd_message("UNLOCKED!           ")

            # red LED off
            red.write(0)
            green.write(1)
            time.sleep(1)

            lcd_send_command(LCD_LINE_2)
            lcd_message("Hello user       ") # change to user's actual name later
            time.sleep(1)
            GLOBAL_SER = "finger lock"
            GLOBAL_FACE = "face lock"

        if GLOBAL_SER == "finger wrong":
            lcd_send_command(LCD_RETURN_HOME)
            lcd_send_command(LCD_TURN_OFF_CURSOR)
            lcd_send_command(LCD_SET_ENTRY_MODE)

            # Write a message to the bottom line of the LCD
            lcd_send_command(LCD_LINE_2)
            lcd_message("Unrecognized!      ")
            flash_red()
            GLOBAL_SER = "finger lock"


        if GLOBAL_KEY == "keypad lock" or GLOBAL_KEY == "gui lock" or GLOBAL_FACE == "face lock" or GLOBAL_SER == "finger lock":
            # Write a message to the bottom line of the LCD
            lcd_send_command(LCD_LINE_2)
            lcd_message("LOCKED        ")

        if GLOBAL_KEY == "keypad entry":
            lcd_send_command(LCD_LINE_2)
            lcd_send_command(LCD_TURN_OFF_CURSOR)
            lcd_send_command(LCD_SET_ENTRY_MODE)
            lcd_message(typed_code + "      ")

        if GLOBAL_KEY == "keypad unlock": #or GLOBAL_KEY == "gui unlock":
            lcd_send_command(LCD_LINE_2)
            lcd_send_command(LCD_TURN_OFF_CURSOR)
            lcd_send_command(LCD_SET_ENTRY_MODE)
            lcd_message("UNLOCKED!  ")
#
#            # red LED off
            red.write(0)
            green.write(1)
#            green.write(0)
            time.sleep(1)
            GLOBAL_KEY == "keypad lock"
            red.write(1)
            green.write(0)


        if GLOBAL_KEY == "keypad wrong":
            lcd_send_command(LCD_LINE_2)
            lcd_send_command(LCD_TURN_OFF_CURSOR)
            lcd_send_command(LCD_SET_ENTRY_MODE)
            lcd_message("INCORRECT!  ")
            flash_red()
            GLOBAL_KEY = "keypad lock"

if __name__ == '__main__':
    lcd_init()

    # turn red LED on
    red.write(1)
    green.write(0)


    print("LCD Starting...")
    time.sleep(1)

    try:
        signal.signal(signal.SIGINT, signal_handler)

        serial_thread = threading.Thread(target=serial_thread_func)
        serial_thread.daemon = True
        serial_thread.start()

        socket_thread = threading.Thread(target=socket_thread_func)
        socket_thread.daemon = True
        socket_thread.start()

        LCD_thread = threading.Thread(target=LCD_thread_func)
        LCD_thread.daemon = True
        LCD_thread.start()

        keypad_thread = threading.Thread(target=keypad_thread_func)
        keypad_thread.daemon = True
        keypad_thread.start()

        print("Begin test...")

        # Wait for the threads to finish
        serial_thread.join()
        socket_thread.join()
        LCD_thread.join()
        keypad_thread.join()

    finally:
        red.write(1)
        green.write(0)
        lcd_send_command(LCD_LINE_2)
        lcd_message("LOCKED        ")
        ser.close()
        socket.close()
#        msg_server.close()
#        context.term()
        image_sender.close()
        video_capture.release()
        cv2.destroyAllWindows()
        print("Sockets closed")
        exit()
