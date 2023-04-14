import mraa
import time

row_pins = [37, 36, 38, 40]
col_pins = [29, 31, 33, 35]

for pin in row_pins:
    mraa.Gpio(pin).dir(mraa.DIR_IN)
for pin in col_pins:
    mraa.Gpio(pin).dir(mraa.DIR_OUT)

keypad = [
    ['1', '4', '7', '*'],
    ['2', '5', '8', '0'],
    ['3', '6', '9', '#'],
    ['A', 'B', 'C', 'D']
]

def read_keypad():
        for i in range(len(col_pins)):
            # Set the current column pin to high
            mraa.Gpio(col_pins[i]).write(1)
            for j in range(len(row_pins)):
                # Read the current row pin
                if mraa.Gpio(row_pins[j]).read() == 1:
                    # Button pressed, print the corresponding key
                    print("Button pressed: ", keypad[j][i])
                    # Add a small delay to debounce the button
                    time.sleep(0.2)
            # Set the current column pin back to low
            mraa.Gpio(col_pins[i]).write(0)

print("Begin...")

while True:
    read_keypad()
