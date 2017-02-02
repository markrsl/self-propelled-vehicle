'''
Created on 2017/2/2

@author: Mark Hsu
'''

import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

ultrasound_Forward_TRIG = 11
ultrasound_Forward_ECHO = 12
ultrasound_Left_TRIG = 13
ultrasound_Left_ECHO = 15
ultrasound_Right_TRIG = 16
ultrasound_Right_ECHO = 18

GPIO.setup(ultrasound_Forward_TRIG, GPIO.OUT)
GPIO.setup(ultrasound_Forward_ECHO, GPIO.IN)
GPIO.setup(ultrasound_Left_TRIG, GPIO.OUT)
GPIO.setup(ultrasound_Left_ECHO, GPIO.IN)
GPIO.setup(ultrasound_Right_TRIG, GPIO.OUT)
GPIO.setup(ultrasound_Right_ECHO, GPIO.IN)

def ultrasound(TRIG,ECHO):
#    GPIO.output(TRIG, 0)
#    time.sleep(0.01)

    GPIO.output(TRIG, 1)
#    time.sleep(0.00001)
    GPIO.output(TRIG, 0)
#    start = time.time()
    while GPIO.input(ECHO) == 0:
        start = time.time()
    while GPIO.input(ECHO) == 1:
        stop = time.time()
    distance = (stop - start) * 34000 / 2
    print(distance)

def main():
    try:
        ultrasound(ultrasound_Forward_TRIG, ultrasound_Forward_ECHO)
        ultrasound(ultrasound_Left_TRIG, ultrasound_Left_ECHO)
        ultrasound(ultrasound_Right_TRIG, ultrasound_Right_ECHO)
    except KeyboardInterrupt:
        GPIO.cleanup()
if __name__ == '__main__':
    main()

