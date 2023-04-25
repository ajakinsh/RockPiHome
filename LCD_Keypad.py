import mraa
import time

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
    lcd_send_command(0x0C)
    time.sleep(0.153)
    lcd_send_command(0x06)
    time.sleep(0.4)
    lcd_send_command(0x02)
    time.sleep(0.4)
    lcd_send_command(0x01)
    time.sleep(0.4)

    lcd_en.write(1)
    lcd_rs.write(1)
    lcd_d0.write(0)
    lcd_d1.write(0)
    lcd_d2.write(0)
    lcd_d3.write(0)
    lcd_d4.write(0)
    lcd_d5.write(0)
    lcd_d6.write(0)
    lcd_d7.write(0)

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

    if col2.read() == 0:
        print("Button pressed: 2")
        time.sleep(0.6)

    if col3.read() == 0:
        print("Button pressed: 3")
        time.sleep(0.6)
        
    if col4.read() == 0:
        print("Button pressed: A")
        time.sleep(0.6)   

    row1.write(1)
    
    #row 2
    row2.write(0)
    if col1.read() == 0:
        print("Button pressed: 4")
        time.sleep(0.6)

    if col2.read() == 0:
        print("Button pressed: 5")
        time.sleep(0.6)

    if col3.read() == 0:
        print("Button pressed: 6")
        time.sleep(0.6)
        
    if col4.read() == 0:
        print("Button pressed: B")
        time.sleep(0.6)   

    row2.write(1)
    
    #row 3
    row3.write(0)
    if col1.read() == 0:
        print("Button pressed: 7")
        time.sleep(0.6)

    if col2.read() == 0:
        print("Button pressed: 8")
        time.sleep(0.6)

    if col3.read() == 0:
        print("Button pressed: 9")
        time.sleep(0.6)
        
    if col4.read() == 0:
        print("Button pressed: C")
        time.sleep(0.6)   

    row3.write(1)
    
    #row 4
    row4.write(0)
    if col1.read() == 0:
        print("Button pressed: *")
        time.sleep(0.6)

    if col2.read() == 0:
        print("Button pressed: 0")
        time.sleep(0.6)

    if col3.read() == 0:
        print("Button pressed: #")
        time.sleep(0.6)
        
    if col4.read() == 0:
        print("Button pressed: D")
        time.sleep(0.6)   

    row4.write(1)

# Saved Door Lock Code 
saved_code = "5678"

# Initialize the typed code variable
typed_code = ""

lcd_init()
print(" LCD Starting...")
time.sleep(1)
print("Begin test...")


while True:

    # Read From Keypad
    key = read_keypad()

    # If a key is presses
    if key:
        typed_code += str(key)
        lcd_send_command(0x01) # Clear display
        lcd_message("Code: " + typed_code) # Print code on LCD

        # Check Code
        if typed_code == saved_code:
            lcd_send_command(0x02) # Return home
            lcd_send_command(0x0C) # Turn off cursor
            lcd_send_command(0x06) # Set entry mode
            lcd_message("UNLOCKED!")
            time.sleep(1)
        else:
            lcd_send_command(0x01) # Clear display
            lcd_send_command(0x02) # Return home
            lcd_send_command(0x0C) # Turn off cursor
            lcd_send_command(0x06) # Set entry mode
            lcd_message("LOCKED. Please try again.")
            time.sleep(1)




































# Define GPIO pin connections for the LCD
RS = 16
EN = 18
D0 = 13
D1 = 15
D2 = 19
D3 = 21
D4 = 23
D5 = 22
D6 = 24
D7 = 26

# Define LCD constants
LCD_WIDTH = 16 # Maximum characters per line
LCD_CHR = mraa.Gpio(RS) # RS pin of the LCD
LCD_CMD = mraa.Gpio(EN) # EN pin of the LCD
LCD_LINES = 2 # Number of lines on the LCD
LCD_DISP = mraa.Lcd(LCD_CHR, LCD_CMD, D0, D1, D2, D3, D4, D5, D6, D7, LCD_LINES, LCD_WIDTH)

# Define the keypad matrix
keys = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

# Define the code to unlock the system
unlock_code = '1234'

# Initialize the LCD
LCD_DISP.begin(LCD_WIDTH, LCD_LINES)
LCD_DISP.clear()

# Define function to print the typed code on the LCD
def print_code(code):
    LCD_DISP.clear()
    LCD_DISP.setCursor(0, 0)
    LCD_DISP.write('CODE: ' + code)

# Define function to check if typed code matches unlock code and print message on LCD
def check_code(code):
    if code == unlock_code:
        LCD_DISP.clear()
        LCD_DISP.setCursor(0, 0)
        LCD_DISP.write('UNLOCKED!')
        time.sleep(2)
        LCD_DISP.clear()
        print_code('')
    else:
        LCD_DISP.clear()
        LCD_DISP.setCursor(0, 0)
        LCD_DISP.write('LOCKED')
        time.sleep(2)
        LCD_DISP.clear()
        print_code('')

# Define function to read the keypad and update the typed code on the LCD
def read_keypad():
    code = ''
    while True:
        for i in range(5):
            mraa.Gpio(i+4).dir(mraa.DIR_OUT)
            mraa.Gpio(i+4).write(1)
            for j in range(4):
                mraa.Gpio(j).dir(mraa.DIR_IN)
                if mraa.Gpio(j).read() == 0:
                    code += keys[i][j]
                    print_code(code)
                    time.sleep(0.3)
            mraa.Gpio(j).dir(mraa.DIR_OUT)
            mraa.Gpio(j).write(1)
        if len(code) == len(unlock_code):
            check_code(code)
            code = ''

# Call the read_keypad function to start the program
read_keypad()
