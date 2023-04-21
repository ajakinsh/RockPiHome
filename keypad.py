import mraa
import time


row1 = mraa.Gpio(29)
row1.dir(mraa.DIR_OUT)
row2 = mraa.Gpio(31)
row2.dir(mraa.DIR_OUT)
row3 = mraa.Gpio(33)
row3.dir(mraa.DIR_OUT)
row4 = mraa.Gpio(35)
row4.dir(mraa.DIR_OUT)


col1 = mraa.Gpio(37)
col1.dir(mraa.DIR_IN)
col2 = mraa.Gpio(36)
col2.dir(mraa.DIR_IN)
col3 = mraa.Gpio(38)
col3.dir(mraa.DIR_IN)
col4 = mraa.Gpio(40)
col4.dir(mraa.DIR_IN)

def read_keypad():
    # row 1 
    row1.write(0)
    if col1.read() == 0:
        print("Button pressed: 1")
        # Add a small delay to debounce the button
        time.sleep(0.6)

    if col2.read() == 0:
        print("Button pressed: 2")
        time.sleep(0.6)

    if col3.read() == 0:
        print("Button pressed: 3")
        time.sleep(0.6)
        
    if col4.read() == 0:
        print("Button pressed: A")
        time.sleep(0.6)   

    row1.write(1)
    
    #row 2
    row2.write(0)
    if col1.read() == 0:
        print("Button pressed: 4")
        time.sleep(0.6)

    if col2.read() == 0:
        print("Button pressed: 5")
        time.sleep(0.6)

    if col3.read() == 0:
        print("Button pressed: 6")
        time.sleep(0.6)
        
    if col4.read() == 0:
        print("Button pressed: B")
        time.sleep(0.6)   

    row2.write(1)
    
    #row 3
    row3.write(0)
    if col1.read() == 0:
        print("Button pressed: 7")
        time.sleep(0.6)

    if col2.read() == 0:
        print("Button pressed: 8")
        time.sleep(0.6)

    if col3.read() == 0:
        print("Button pressed: 9")
        time.sleep(0.6)
        
    if col4.read() == 0:
        print("Button pressed: C")
        time.sleep(0.6)   

    row3.write(1)
    
    #row 4
    row4.write(0)
    if col1.read() == 0:
        print("Button pressed: *")
        time.sleep(0.6)

    if col2.read() == 0:
        print("Button pressed: 0")
        time.sleep(0.6)

    if col3.read() == 0:
        print("Button pressed: #")
        time.sleep(0.6)
        
    if col4.read() == 0:
        print("Button pressed: D")
        time.sleep(0.6)   

    row4.write(1)

print("Begin...")

while True:
    read_keypad()
