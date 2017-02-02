'''
Created on 2017/2/2
@author: Mark Hsu
'''
import time
import RPi.GPIO as GPIO
from curses.ascii import DLE

# Physical numbering
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

# Define GPIO
ultrasound_Forward_TRIG = 11
ultrasound_Forward_ECHO = 12
ultrasound_Left_TRIG = 13
ultrasound_Left_ECHO = 15
ultrasound_Right_TRIG = 16
ultrasound_Right_ECHO = 18
motor_RightFront_in1 = 31
motor_RightFront_in2 = 33
motor_RightRear_in3 = 35
motor_RightRear_in4 = 37
motor_LeftFront_in1 = 32
motor_LeftFront_in2 = 36
motor_LeftRear_in3 = 38
motor_LeftRear_in4 = 40
# setup GPIO
GPIO.setup(ultrasound_Forward_TRIG, GPIO.OUT)
GPIO.setup(ultrasound_Forward_ECHO, GPIO.IN)
GPIO.setup(ultrasound_Left_TRIG, GPIO.OUT)
GPIO.setup(ultrasound_Left_ECHO, GPIO.IN)
GPIO.setup(ultrasound_Right_TRIG, GPIO.OUT)
GPIO.setup(ultrasound_Right_ECHO, GPIO.IN)
GPIO.setup(motor_RightFront_in1, GPIO.OUT)
GPIO.setup(motor_RightFront_in2, GPIO.OUT)
GPIO.setup(motor_RightRear_in3, GPIO.OUT)
GPIO.setup(motor_RightRear_in4, GPIO.OUT)
GPIO.setup(motor_LeftFront_in1, GPIO.OUT)
GPIO.setup(motor_LeftFront_in2, GPIO.OUT)
GPIO.setup(motor_LeftRear_in3, GPIO.OUT)
GPIO.setup(motor_LeftRear_in4, GPIO.OUT)

def ultrasound(TRIG, ECHO):
    GPIO.output(TRIG, 0)
    time.sleep(0.01)
    GPIO.output(TRIG, 1)
    time.sleep(0.00001)
    GPIO.output(TRIG, 0)
    start = time.time()
    while GPIO.input(ECHO) == 0:
        start = time.time()
    while GPIO.input(ECHO) == 1:
        stop = time.time()
    distance = (stop - start) * 34000 / 2
    return distance

def forward():
    GPIO.output(motor_RightFront_in1, False)
    GPIO.output(motor_RightFront_in2, True)
    GPIO.output(motor_RightRear_in3, False)
    GPIO.output(motor_RightRear_in4, True)
    GPIO.output(motor_LeftFront_in1, True)
    GPIO.output(motor_LeftFront_in2, False)
    GPIO.output(motor_LeftRear_in3, True)
    GPIO.output(motor_LeftRear_in4, False)

def backward():
    stop()
    time.sleep(0.1)
    GPIO.output(motor_RightFront_in1, True)
    GPIO.output(motor_RightFront_in2, False)
    GPIO.output(motor_RightRear_in3, True)
    GPIO.output(motor_RightRear_in4, False)
    GPIO.output(motor_LeftFront_in1, False)
    GPIO.output(motor_LeftFront_in2, True)
    GPIO.output(motor_LeftRear_in3, False)
    GPIO.output(motor_LeftRear_in4, True)

def stop():
    GPIO.output(motor_RightFront_in1, False)
    GPIO.output(motor_RightFront_in2, False)
    GPIO.output(motor_RightRear_in3, False)
    GPIO.output(motor_RightRear_in4, False)
    GPIO.output(motor_LeftFront_in1, False)
    GPIO.output(motor_LeftFront_in2, False)
    GPIO.output(motor_LeftRear_in3, False)
    GPIO.output(motor_LeftRear_in4, False)

def left():
    stop()
    GPIO.output(motor_RightFront_in1, False)
    GPIO.output(motor_RightFront_in2, True)
    GPIO.output(motor_RightRear_in3, False)
    GPIO.output(motor_RightRear_in4, True)

def right():
    stop()
    GPIO.output(motor_LeftFront_in1, True)
    GPIO.output(motor_LeftFront_in2, False)
    GPIO.output(motor_LeftRear_in3, True)
    GPIO.output(motor_LeftRear_in4, False)
def left4WD():
    stop()
    time.sleep(0.1)
    GPIO.output(motor_RightFront_in1, False)
    GPIO.output(motor_RightFront_in2, True)
    GPIO.output(motor_RightRear_in3, False)
    GPIO.output(motor_RightRear_in4, True)
    GPIO.output(motor_LeftFront_in1, False)
    GPIO.output(motor_LeftFront_in2, True)
    GPIO.output(motor_LeftRear_in3, False)
    GPIO.output(motor_LeftRear_in4, True)
def right4WD():
    stop()
    time.sleep(0.1)
    GPIO.output(motor_RightFront_in1, True)
    GPIO.output(motor_RightFront_in2, False)
    GPIO.output(motor_RightRear_in3, True)
    GPIO.output(motor_RightRear_in4, False)
    GPIO.output(motor_LeftFront_in1, True)
    GPIO.output(motor_LeftFront_in2, False)
    GPIO.output(motor_LeftRear_in3, True)
    GPIO.output(motor_LeftRear_in4, False)
    
dSafeForward = 50
dSafeSide = 10
def main():
    try:
        while True:
            dforward = ultrasound(ultrasound_Forward_TRIG, ultrasound_Forward_ECHO)
            dLeft = ultrasound(ultrasound_Left_TRIG, ultrasound_Left_ECHO)
            dRight = ultrasound(ultrasound_Right_TRIG, ultrasound_Right_ECHO)
            print('forward:{} \t left:{} \t right:{}'.format(dforward, dLeft, dRight))
            
            if dforward < dSafeForward and dLeft < dSafeSide and dRight < dSafeSide:
                stop()
                print("Here is not safe!!!")
            elif dforward < dSafeForward and dLeft < dSafeSide and dRight > dSafeSide:
                right4WD()
                print("Turn RIGHT!!!")
            elif dforward < dSafeForward and dLeft > dSafeSide and dRight < dSafeSide:
                left4WD()
                print("Turn Left!!!")
            elif dforward < dSafeForward and dLeft > dSafeSide and dRight > dSafeSide:         
                if dLeft >= dRight:
                    left4WD()
                    print("Turn Left!!!")
                elif dLeft < dRight:
                    right4WD()
                    print("Turn RIGHT!!!")
            elif dforward > dSafeForward:
                forward()
                print('Keep moving!')
    except KeyboardInterrupt:
        print('Bye')
    finally:
        stop()
        GPIO.cleanup()
if __name__ == '__main__':
    main()

