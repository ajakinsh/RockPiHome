import Adafruit_CharLCD as LCD
import time

# Initialize the LCD using the pins of your choice
lcd_rs = 27
lcd_en = 22
lcd_d4 = 25
lcd_d5 = 24
lcd_d6 = 23
lcd_d7 = 18
lcd_columns = 16
lcd_rows = 2
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows)

# Write a message to the LCD
lcd.clear()
lcd.message('locked')
time.sleep(2)

# Clear the LCD and write a different message
while True:
    lcd.clear()
    lcd.message('unlocked')
    time.sleep(2)

# Clear the LCD when done
# lcd.clear()