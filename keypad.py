import mraa
import time

# Define the row and column pins
row_pins = [37, 36, 38, 40]
col_pins = [29, 31, 33, 35]

# Initialize the row pins as input and the column pins as output
for pin in row_pins:
    mraa.Gpio(pin).dir(mraa.DIR_IN)
for pin in col_pins:
    mraa.Gpio(pin).dir(mraa.DIR_OUT)

# Define the keypad matrix
keypad = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

# Function to read the keypad and detect button presses
def read_keypad():
    while True:
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

# Call the function to read the keypad
read_keypad()
