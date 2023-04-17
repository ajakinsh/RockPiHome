import mraa
import time

# Define row and column pin numbers
ROW_PINS = [37, 36, 38, 40]
COL_PINS = [29, 31, 33, 35]

# Initialize row and column GPIOs
row_gpio = []
col_gpio = []
for pin in ROW_PINS:
    row_gpio.append(mraa.Gpio(pin))
for pin in COL_PINS:
    col_gpio.append(mraa.Gpio(pin))

# Configure row GPIOs as inputs and column GPIOs as outputs
for gpio in row_gpio:
    gpio.dir(mraa.DIR_IN)
for gpio in col_gpio:
    gpio.dir(mraa.DIR_OUT)

# Define the keypad matrix
KEYS = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

# Function to read keypad input
def read_keypad():
    while True:
        for i in range(4):
            # Set column low
            col_gpio[i].write(0)
            for j in range(4):
                # Read row input
                if row_gpio[j].read() == 0:
                    # Return the corresponding key
                    return KEYS[j][i]
            # Set column high
            col_gpio[i].write(1)
        time.sleep(0.1)

# Main loop
while True:
    key = read_keypad()
    print("Key pressed: " + key)
