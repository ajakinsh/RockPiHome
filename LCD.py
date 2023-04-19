import RPi.GPIO as GPIO
import time
import Adafruit_CharLCD as LCD
 
# Initialize the LCD screen
lcd_rs = 26
lcd_en = 19
lcd_d4 = 13
lcd_d5 = 6
lcd_d6 = 5
lcd_d7 = 11
lcd_backlight = 4
lcd_columns = 16
lcd_rows = 2
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows, lcd_backlight)
 
# Set up the keypad
MATRIX = [[1, 2, 3, "A"],
          [4, 5, 6, "B"],
          [7, 8, 9, "C"],
          ["*", 0, "#", "D"]]
 
ROW = [4, 17, 27, 22]
COL = [18, 23, 24, 25]
 
for j in range(4):
    GPIO.setup(COL[j], GPIO.OUT)
    GPIO.output(COL[j], 1)
 
for i in range(4):
    GPIO.setup(ROW[i], GPIO.IN, pull_up_down=GPIO.PUD_UP)
 
# Define the saved string code
saved_code = "1234"
 
# Define a function to get the character corresponding to the button pressed
def get_key():
    for j in range(4):
        GPIO.output(COL[j], 0)
 
        for i in range(4):
            if GPIO.input(ROW[i]) == 0:
                return MATRIX[i][j]
 
        GPIO.output(COL[j], 1)
 
    return None
 
# Initialize the typed code variable
typed_code = ""
 
# Continuously read the keypad and display the typed code on the LCD screen
while True:
    key = get_key()
    if key:
        typed_code += str(key)
        lcd.clear()
        lcd.message("Code: " + typed_code)
 
        if typed_code == saved_code:
            lcd.set_cursor(0, 1)
            lcd.message("UNLOCKED!")
        else:
            lcd.set_cursor(0, 1)
            lcd.message("LOCKED")
 
        time.sleep(0.5)
