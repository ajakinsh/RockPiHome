import mraa
import time
from datetime import datetime, timedelta
import serial
import threading

# Define the possible serial port names
port1 = '/dev/ttyACM0'
port2 = '/dev/ttyACM1'
baudrate = 57600

GLOBAL_SER = None
GLOBAL_KEY = "keypad lock"

# set initial time
last_command_time = datetime.now()

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

def read_serial_thread_func():
    global last_command_time

    while True:
        try: #large try-except block used for closing things properly after a keyboard interrupt
            if ser.in_waiting > 0:
                # read from serial port
                ser_data = ser.readline().decode().rstrip()
                print("(Serial)\t", ser_data)

                # Check if message indicates a fingerprint match; update LCD
                if "Found ID #" in ser_data:
                    global GLOBAL_SER
                    GLOBAL_SER = "finger unlock"

            # check if it's time to send the command
            if datetime.now() - last_command_time >= timedelta(seconds=1):  # send command every second
                ser.write("C\n".encode())
                last_command_time = datetime.now()

        except KeyboardInterrupt:
            # If the user presses Ctrl-C, stop the thread
            break
    return

def keypad_thread_func():
    global GLOBAL_KEY
    global typed_code
    while True:
        try:
            # Read From Keypad
            key = read_keypad()
            if key:
                typed_code += str(key)
                GLOBAL_KEY = "keypad entry"


            if len(typed_code) == 4:
                if typed_code == saved_code:
                    GLOBAL_KEY = "keypad unlock"
                    print("Correct code")
                    typed_code = ""
                else:
                    GLOBAL_KEY = "keypad wrong"
                    print("Incorrect code")
                    typed_code = ""
        except KeyboardInterrupt:
            break
    return

def LCD_thread_func():
    global GLOBAL_SER
    global GLOBAL_KEY
    global typed_code
    while True:
        try:
            # Get the current time and format it as a string
            current_time = datetime.now().strftime('%H:%M:%S')

            # Write the current time to the top line of the LCD
            lcd_send_command(LCD_RETURN_HOME)
            lcd_send_command(LCD_TURN_OFF_CURSOR)
            lcd_send_command(LCD_SET_ENTRY_MODE)
            lcd_message(current_time + "    ")

            # red led on; green LED off

            if GLOBAL_SER == "finger unlock":
                lcd_send_command(LCD_RETURN_HOME)
                lcd_send_command(LCD_TURN_OFF_CURSOR)
                lcd_send_command(LCD_SET_ENTRY_MODE)

                # Write a message to the bottom line of the LCD
                lcd_send_command(LCD_LINE_2)
                lcd_message("UNLOCKED!           ")

                # turn on a green LED; red LED off

                time.sleep(1)
                lcd_send_command(LCD_LINE_2)
                lcd_message("Hello user       ") # change to user's actual name later

                time.sleep(2)
                GLOBAL_SER = "finger lock"

            
            if GLOBAL_KEY == "keypad lock":
                # Write a message to the bottom line of the LCD
                lcd_send_command(LCD_LINE_2)
                lcd_message("LOCKED        ")
            
            
            if GLOBAL_KEY == "keypad entry":
                lcd_send_command(LCD_LINE_2)
                lcd_send_command(LCD_TURN_OFF_CURSOR)
                lcd_send_command(LCD_SET_ENTRY_MODE)
                lcd_message(typed_code + "      ")

            if GLOBAL_KEY == "keypad unlock":
                lcd_send_command(LCD_LINE_2)
                lcd_send_command(LCD_TURN_OFF_CURSOR)
                lcd_send_command(LCD_SET_ENTRY_MODE)
                lcd_message("UNLOCKED!  ")
                # turn on a green LED; red LED off


            if GLOBAL_KEY == "keypad wrong":
                lcd_send_command(LCD_LINE_2)
                lcd_send_command(LCD_TURN_OFF_CURSOR)
                lcd_send_command(LCD_SET_ENTRY_MODE)
                lcd_message("INCORRECT!  ")
                GLOBAL_KEY = "keypad lock"

        except KeyboardInterrupt:
            break
    return


lcd_init()

# turn red LED on; green LED off

print("LCD Starting...")
time.sleep(1)

read_serial_thread = threading.Thread(target=read_serial_thread_func)
read_serial_thread.daemon = True
read_serial_thread.start()

LCD_thread = threading.Thread(target=LCD_thread_func)
LCD_thread.daemon = True
LCD_thread.start()

keypad_thread = threading.Thread(target=keypad_thread_func)
keypad_thread.daemon = True
keypad_thread.start()

print("Begin test...")

# Wait for the threads to finish
read_serial_thread.join()
LCD_thread.join()
keypad_thread.join()

ser.close()
exit()
