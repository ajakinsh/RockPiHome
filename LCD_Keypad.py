import mraa
import time

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
