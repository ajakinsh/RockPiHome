import mraa
import time

# LCD dimensions
LCD_ROWS = 2
LCD_COLS = 16

# LCD commands
LCD_CLEAR_DISPLAY = 0x01
LCD_RETURN_HOME = 0x02
LCD_ENTRY_MODE_SET = 0x04
LCD_DISPLAY_ON_OFF_CONTROL = 0x08
LCD_FUNCTION_SET = 0x20
LCD_SET_CGRAM_ADDR = 0x40
LCD_SET_DDRAM_ADDR = 0x80

# LCD flags for function set
LCD_8BIT_MODE = 0x10
LCD_2LINE_MODE = 0x08
LCD_FONT_5X8 = 0x00

# GPIO pins
LCD_RS_PIN = 8
LCD_E_PIN = 9
LCD_D0_PIN = 10
LCD_D1_PIN = 11
LCD_D2_PIN = 12
LCD_D3_PIN = 13
LCD_D4_PIN = 14
LCD_D5_PIN = 15
LCD_D6_PIN = 16
LCD_D7_PIN = 17

# Initialize GPIO pins
rs_pin = mraa.Gpio(LCD_RS_PIN)
rs_pin.dir(mraa.DIR_OUT)
e_pin = mraa.Gpio(LCD_E_PIN)
e_pin.dir(mraa.DIR_OUT)
d0_pin = mraa.Gpio(LCD_D0_PIN)
d0_pin.dir(mraa.DIR_OUT)
d1_pin = mraa.Gpio(LCD_D1_PIN)
d1_pin.dir(mraa.DIR_OUT)
d2_pin = mraa.Gpio(LCD_D2_PIN)
d2_pin.dir(mraa.DIR_OUT)
d3_pin = mraa.Gpio(LCD_D3_PIN)
d3_pin.dir(mraa.DIR_OUT)
d4_pin = mraa.Gpio(LCD_D4_PIN)
d4_pin.dir(mraa.DIR_OUT)
d5_pin = mraa.Gpio(LCD_D5_PIN)
d5_pin.dir(mraa.DIR_OUT)
d6_pin = mraa.Gpio(LCD_D6_PIN)
d6_pin.dir(mraa.DIR_OUT)
d7_pin = mraa.Gpio(LCD_D7_PIN)
d7_pin.dir(mraa.DIR_OUT)

# Write an 8-bit value to the LCD
def lcd_write_8bits(value):
    d0_pin.write((value >> 0) & 0x01)
    d1_pin.write((value >> 1) & 0x01)
    d2_pin.write((value >> 2) & 0x01)
    d3_pin.write((value >> 3) & 0x01)
    d4_pin.write((value >> 4) & 0x01)
    d5_pin.write((value >> 5) & 0x01)
    d6_pin.write((value >> 6) & 0x01)
    d7_pin.write((value >> 7) & 0x01)
    e_pin.write(1)
    time.sleep(0.0001)
    e_pin.write(0)
    time.sleep(0.0001)

# Write an 8-bit command to the LCD
def lcd_write_cmd(cmd):
    rs_pin.write(0)
    lcd_write_8bits(cmd)

# Write an 8-bit character to the LCD
def lcd_write_char(char):
    rs_pin.write(1)
    lcd_write_8bits(char)

# Initialize
def lcd_init():
  # Wait for the LCD to power up
  time.sleep(0.05)
  lcd_write_cmd(LCD_FUNCTION_SET | LCD_8BIT_MODE | LCD_2LINE_MODE | LCD_FONT_5X8)
  time.sleep(0.0045)
  
  #Display Off
  lcd_write_cmd(LCD_DISPLAY_ON_OFF_CONTROL | 0x04)
  
  # Clear display
  lcd_write_cmd(LCD_CLEAR_DISPLAY)
  time.sleep(0.002)
  
  # Entry mode set
  lcd_write_cmd(LCD_ENTRY_MODE_SET | 0x06)
# lcd_write_cmd(LCD_ENTRY_MODE_SET | 0x02)
  
  # Display on
  lcd_write_cmd(LCD_DISPLAY_ON_OFF_CONTROL | 0x04)
  
#Print a string to the LCD
def lcd_print(string):
  for char in string:
  lcd_write_char(ord(char))

lcd_init()
lcd_print("Hello")

"""
# Print "Hello" on the LCD
lcd_write_char(ord('H'))
lcd_write_char(ord('e'))
lcd_write_char(ord('l'))
lcd_write_char(ord('l'))
lcd_write_char(ord('o'))"""
