'''
Created on 2017¦~2¤ë3¤é

@author: Administrator
'''
import RPi.GPIO as GPIO
import time
class vehicle():
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
    def __init__(self):
        pass
    @staticmethod
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
    @staticmethod
    def forward(cls):
        GPIO.output(cls.motor_RightFront_in1, False)
        GPIO.output(cls.motor_RightFront_in2, True)
        GPIO.output(cls.motor_RightRear_in3, False)
        GPIO.output(cls.motor_RightRear_in4, True)
        GPIO.output(cls.motor_LeftFront_in1, True)
        GPIO.output(cls.motor_LeftFront_in2, False)
        GPIO.output(cls.motor_LeftRear_in3, True)
        GPIO.output(cls.motor_LeftRear_in4, False)
    @staticmethod
    def backward(cls):
        GPIO.output(cls.motor_RightFront_in1, True)
        GPIO.output(cls.motor_RightFront_in2, False)
        GPIO.output(cls.motor_RightRear_in3, True)
        GPIO.output(cls.motor_RightRear_in4, False)
        GPIO.output(cls.motor_LeftFront_in1, False)
        GPIO.output(cls.motor_LeftFront_in2, True)
        GPIO.output(cls.motor_LeftRear_in3, False)
        GPIO.output(cls.motor_LeftRear_in4, True)
    @staticmethod
    def stop(cls):
        GPIO.output(cls.motor_RightFront_in1, False)
        GPIO.output(cls.motor_RightFront_in2, False)
        GPIO.output(cls.motor_RightRear_in3, False)
        GPIO.output(cls.motor_RightRear_in4, False)
        GPIO.output(cls.motor_LeftFront_in1, False)
        GPIO.output(cls.motor_LeftFront_in2, False)
        GPIO.output(cls.motor_LeftRear_in3, False)
        GPIO.output(cls.motor_LeftRear_in4, False)
    @staticmethod
    def left(cls):
        GPIO.output(cls.motor_RightFront_in1, False)
        GPIO.output(cls.motor_RightFront_in2, True)
        GPIO.output(cls.motor_RightRear_in3, False)
        GPIO.output(cls.motor_RightRear_in4, True)
    @staticmethod
    def right(cls):
        GPIO.output(cls.motor_LeftFront_in1, True)
        GPIO.output(cls.motor_LeftFront_in2, False)
        GPIO.output(cls.motor_LeftRear_in3, True)
        GPIO.output(cls.motor_LeftRear_in4, False)
    @staticmethod
    def left4WD(cls):
        GPIO.output(cls.motor_RightFront_in1, False)
        GPIO.output(cls.motor_RightFront_in2, True)
        GPIO.output(cls.motor_RightRear_in3, False)
        GPIO.output(cls.motor_RightRear_in4, True)
        GPIO.output(cls.motor_LeftFront_in1, False)
        GPIO.output(cls.motor_LeftFront_in2, True)
        GPIO.output(cls.motor_LeftRear_in3, False)
        GPIO.output(cls.motor_LeftRear_in4, True)
    @staticmethod
    def right4WD(cls):
        GPIO.output(cls.motor_RightFront_in1, True)
        GPIO.output(cls.motor_RightFront_in2, False)
        GPIO.output(cls.motor_RightRear_in3, True)
        GPIO.output(cls.motor_RightRear_in4, False)
        GPIO.output(cls.motor_LeftFront_in1, True)
        GPIO.output(cls.motor_LeftFront_in2, False)
        GPIO.output(cls.motor_LeftRear_in3, True)
        GPIO.output(cls.motor_LeftRear_in4, False)
    @staticmethod
    def exit():
        GPIO.cleanup()