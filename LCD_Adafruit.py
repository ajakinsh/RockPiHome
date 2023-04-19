import board
import digitalio
import adafruit_character_lcd.character_lcd as characterlcd
import time

# Modify this if you have a different sized character LCD
lcd_columns = 16
lcd_rows = 2

# Define the LCD pins
lcd_rs = digitalio.DigitalInOut(board.D2)
lcd_en = digitalio.DigitalInOut(board.D4)
lcd_d0 = digitalio.DigitalInOut(board.C6)
lcd_d1 = digitalio.DigitalInOut(board.C5)
lcd_d2 = digitalio.DigitalInOut(board.B0)
lcd_d3 = digitalio.DigitalInOut(board.A7)
lcd_d4 = digitalio.DigitalInOut(board.B1)
lcd_d5 = digitalio.DigitalInOut(board.D5)
lcd_d6 = digitalio.DigitalInOut(board.B2)
lcd_d7 = digitalio.DigitalInOut(board.D7) #Need to change, pin 26 has no board GPIO name)

# Initialize the LCD class
lcd = characterlcd.Character_LCD_8bit(
    lcd_rs, lcd_en, lcd_d0, lcd_d1, lcd_d2, lcd_d3, lcd_d4, lcd_d5, lcd_d6, lcd_d7, lcd_columns, lcd_rows
)

# Write a message to the LCD
lcd.clear()
lcd.message = "locked"
time.sleep(2)

# Clear the LCD and write a different message
lcd.clear()
lcd.message = "unlocked"
time.sleep(2)

# Clear the LCD when done
lcd.clear()