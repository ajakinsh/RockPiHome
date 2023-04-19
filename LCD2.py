import mraa
import time

# Define LCD pins
rs_pin = 16
en_pin = 18
d0_pin = 13
d1_pin = 15
d2_pin = 19
d3_pin = 21
d4_pin = 23
d5_pin = 22
d6_pin = 24
d7_pin = 26

# Initialize LCD
lcd = mraa.Gpio(rs_pin)
lcd.dir(mraa.DIR_OUT)
lcd.write(0)
lcd = mraa.Gpio(en_pin)
lcd.dir(mraa.DIR_OUT)
lcd.write(0)
lcd_data_pins = [
    mraa.Gpio(d0_pin),
    mraa.Gpio(d1_pin),
    mraa.Gpio(d2_pin),
    mraa.Gpio(d3_pin),
    mraa.Gpio(d4_pin),
    mraa.Gpio(d5_pin),
    mraa.Gpio(d6_pin),
    mraa.Gpio(d7_pin)
]
for pin in lcd_data_pins:
    pin.dir(mraa.DIR_OUT)
    pin.write(0)

# Define keypad pins and values
rows = [31, 33, 35, 37]
cols = [29, 32, 36, 38]
keypad_vals = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

# Initialize keypad
row_pins = []
for row_pin in rows:
    row = mraa.Gpio(row_pin)
    row.dir(mraa.DIR_OUT)
    row.write(1)
    row_pins.append(row)
col_pins = []
for col_pin in cols:
    col = mraa.Gpio(col_pin)
    col.dir(mraa.DIR_IN)
    col_mode = mraa.MODE_PULLUP
    col_mode |= mraa.MODE_EDGE_BOTH
    col.isr(mraa.EDGE_BOTH, lambda _: None)
    col_pins.append(col)

# Define saved code
saved_code = '1234'

# Initialize variables
lcd_text = ''
typed_code = ''

# Main loop
while True:
    # Check for key presses
    for i, row_pin in enumerate(row_pins):
        row_pin.write(0)
        for j, col_pin in enumerate(col_pins):
            if col_pin.read() == 0:
                lcd_text = keypad_vals[i][j]
                typed_code += lcd_text
                time.sleep(0.1)  # debounce delay
                while col_pin.read() == 0:
                    pass  # wait for key release
        row_pin.write(1)
    
    # Update LCD display
    lcd.write(0)
    lcd.write(1)
    for i, char in enumerate(lcd_text.ljust(16)):
        lcd_data_pins[i].write(ord(char))
    time.sleep(0.1)
    lcd.write(0)
    
    # Check typed code against saved code
    if typed_code == saved_code:
        print("UNLOCKED!")
        # add code to unlock mechanism here
        break
    else:
        print("LOCKED")

# Clean up
lcd.write(0)
for pin in lcd_data_pins:
    pin.write(0)
for pin in row_pins:
    pin.write(1)
for pin in col_pins:
    pin.isr_exit()
