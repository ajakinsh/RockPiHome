import mraa
import time

button = mraa.Gpio(11)
red = mraa.Gpio(24)

button.dir(mraa.DIR_IN)

red.dir(mraa.DIR_OUT)

# toggle both gpio's
while True:
    red.write(1)
    val = button.read()
    print(val)
 