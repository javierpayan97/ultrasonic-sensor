import RPi.GPIO as GPIO
import time
import numpy as np
from RPLCD import CharLCD
def distance():
    GPIO.output(GPIO_TRIGGER,False)
    while GPIO.input(GPIO_ECHO)==False:
        start = time.time()
    while GPIO.input(GPIO_ECHO)==True:
        end = time.time()
    slapsed_time=end-start
    distance = round(slapsed_time/0.000058,2)
    return distance

def display(d):
    lcd.clear()
    lcd.cursor_pos = (0, 0)
    lcd.write_string("Min Distance:")
    lcd.cursor_pos = (1, 0)
    lcd.write_string("{0} cm".format(d))
    
GPIO.cleanup()
me.sleep(5)
GPIO.setmode(GPIO.BOARD)
GPIO_TRIGGER = 16
GPIO_ECHO = 18
limit = 16
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
control_pins=[29,11,13,15]
counter=0
steps = 4*64
arr =[]
nPins=len(control_pins)

lcd = CharLCD(numbering_mode=GPIO.BOARD,cols=16,rows=2,pin_rs=37, pin_e=35, pins_data=[33, 31, 40, 23])
for pin in control_pins:
    GPIO.setup(pin,GPIO.OUT)
    GPIO.output(pin,0)

full_step = [
    [1,0,0,1],
    [0,0,1,1],
    [0,1,1,0],
    [1,1,0,0]
    ]

n=len(full_step)
GPIO.output(GPIO_TRIGGER,True)
dist = distance()
arr.append(dist)
print(dist)
for i in range(steps*2):
    for step in range(n):
        GPIO.output(control_pins[0], full_step[step][0])
        GPIO.output(control_pins[1], full_step[step][1])
        GPIO.output(control_pins[2], full_step[step][2])
        GPIO.output(control_pins[3], full_step[step][3])
        GPIO.output(GPIO_TRIGGER,True)
        time.sleep(0.01)
    if counter ==limit:
        dist = distance()
        arr.append(dist)
        print(dist)
        counter = 0
    counter+=1
a = np.array(arr)
b = len(arr) - a.argmin()
minimum = a.min()
display(minimum)
time.sleep(5)
Fsteps = limit*b
full_step = [
    [1,1,0,0],
    [0,1,1,0],
    [0,0,1,1],
    [1,0,0,1]
    ]
for i in range(Fsteps):
    for step in range(n):
        for pin in range(nPins):
            GPIO.output(control_pins[pin], full_step[step][pin])
        time.sleep(0.01)
