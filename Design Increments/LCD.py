import mraa
import time

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

# Set pin directions
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


lcd_init()
print("Starting...")

while True:
    # Write a message to the LCD
    lcd_send_command(0x01) # Clear display
    lcd_send_command(0x02) # Return home
    lcd_send_command(0x0C) # Turn off cursor
    lcd_send_command(0x06) # Set entry mode
    lcd_message("locked")
    time.sleep(1)

    # Clear the LCD and write a different message
    lcd_send_command(0x01) # Clear display
    lcd_send_command(0x02) # Return home
    lcd_send_command(0x0C) # Turn off cursor
    lcd_send_command(0x06) # Set entry mode
    lcd_message("unlocked")
    time.sleep(1)
