'''
Created on 2017/2/2
@author: Mark Hsu
'''
import time
import RPi.GPIO as GPIO

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
pwmRF = GPIO.PWM(motor_RightFront_in2, 500)
pwmRR = GPIO.PWM(motor_RightRear_in4, 500)
pwmLF = GPIO.PWM(motor_LeftFront_in1, 500)
pwmLR = GPIO.PWM(motor_LeftRear_in3, 500)
pwmRF_Reverse = GPIO.PWM(motor_RightFront_in1, 500)
pwmRR_Reverse = GPIO.PWM(motor_RightRear_in3, 500)
pwmLF_Reverse = GPIO.PWM(motor_LeftFront_in2, 500)
pwmLR_Reverse = GPIO.PWM(motor_LeftRear_in4, 500)
pwmRF.start(0)
pwmRR.start(0)
pwmLF.start(0)
pwmLR.start(0)
pwmRF_Reverse.start(0)
pwmRR_Reverse.start(0)
pwmLF_Reverse.start(0)
pwmLR_Reverse.start(0)

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

def drive(duty):
    pwmLF.ChangeDutyCycle(duty)
    pwmLR.ChangeDutyCycle(duty)
    pwmRF.ChangeDutyCycle(duty)
    pwmRR.ChangeDutyCycle(duty)

def reverse(duty):
    pwmLF_Reverse.ChangeDutyCycle(duty)
    pwmLR_Reverse.ChangeDutyCycle(duty)
    pwmRF_Reverse.ChangeDutyCycle(duty)
    pwmRR_Reverse.ChangeDutyCycle(duty)
    
def right(duty):
    pwmRF.ChangeDutyCycle(duty)
    pwmRR.ChangeDutyCycle(duty)
    
def left(duty):
    pwmLF.ChangeDutyCycle(duty)
    pwmLR.ChangeDutyCycle(duty)
    
def parking():
    drive(0)
    reverse(0)
    
dSafeForward = 50
dSafeSide = 10

def main():
    try:
        while True:
            try:
                duty = int(input("Enter Duty -100 to 100 : "))
                if duty > 100 or duty < -100:
                    duty = None 
            except Exception:
                print("Value error")
            
            if duty > 0:
                drive(duty)
            elif duty == 0:
                parking()
            elif duty < 0:
                reverse(abs(duty))
            
            
#             dforward = ultrasound(ultrasound_Forward_TRIG, ultrasound_Forward_ECHO)
#             dLeft = ultrasound(ultrasound_Left_TRIG, ultrasound_Left_ECHO)
#             dRight = ultrasound(ultrasound_Right_TRIG, ultrasound_Right_ECHO)
#             print('forward:{} \t left:{} \t right:{}'.format(dforward, dLeft, dRight))
#              
#             if dforward < dSafeForward and dLeft < dSafeSide and dRight < dSafeSide:
#                 stop()
#                 print("Here is not safe!!!")
#             elif dforward < dSafeForward and dLeft < dSafeSide and dRight > dSafeSide:
#                 stop()
#                 time.sleep(0.5)
#                 for i in range(31000):
#                     right4WD()
#                 print("Turn RIGHT!!!")
#             elif dforward < dSafeForward and dLeft > dSafeSide and dRight < dSafeSide:
#                 stop()
#                 time.sleep(0.5)
#                 for i in range(31000):
#                     left4WD()
#                 print("Turn Left!!!")
#             elif dforward < dSafeForward and dLeft > dSafeSide and dRight > dSafeSide:
#                 stop()
#                 time.sleep(0.5)         
#                 if dLeft >= dRight:
#                     for i in range(31000):
#                         left4WD()
#                     print("Turn Left!!!")
#                 elif dLeft < dRight:
#                     for i in range(31000):
#                         right4WD()
#                     print("Turn RIGHT!!!")
#             elif dforward > dSafeForward:
#                 forward()
#                 print('Keep moving!')
    except KeyboardInterrupt:
        print('Bye')
    finally:
        pwmRF.stop()
        pwmRR.stop()
        pwmLF.stop()
        pwmLR.stop()
        pwmRF_Reverse.stop()
        pwmRR_Reverse.stop()
        pwmLF_Reverse.stop()
        pwmLR_Reverse.stop()
        GPIO.cleanup()
if __name__ == '__main__':
    main()
