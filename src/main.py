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
dictOut = {
    'ultrasound_Center_TRIG':11,
    'ultrasound_Left_TRIG':13,
    'ultrasound_Right_TRIG':16,
    'motor_RightFront_in1':31,
    'motor_RightFront_in2':33,
    'motor_RightRear_in3':35,
    'motor_RightRear_in4':37,
    'motor_LeftFront_in1':32,
    'motor_LeftFront_in2':36,
    'motor_LeftRear_in3':38,
    'motor_LeftRear_in4':40
    }
dictIn = {
    'ultrasound_Center_ECHO':12,
    'ultrasound_Left_ECHO':15,
    'ultrasound_Right_ECHO':18
    }
# To setup GPIO
GPIO.setup(list(dictOut.values()), GPIO.OUT)
GPIO.setup(list(dictIn.values()), GPIO.IN)
# To create PWM instance
pwmRF = GPIO.PWM(dictOut['motor_RightFront_in2'], 500)
pwmRR = GPIO.PWM(dictOut['motor_RightRear_in4'], 500)
pwmLF = GPIO.PWM(dictOut['motor_LeftFront_in1'], 500)
pwmLR = GPIO.PWM(dictOut['motor_LeftRear_in3'], 500)
pwmRF_Reverse = GPIO.PWM(dictOut['motor_RightFront_in1'], 500)
pwmRR_Reverse = GPIO.PWM(dictOut['motor_RightRear_in3'], 500)
pwmLF_Reverse = GPIO.PWM(dictOut['motor_LeftFront_in2'], 500)
pwmLR_Reverse = GPIO.PWM(dictOut['motor_LeftRear_in4'], 500)
# To start PWM
pwmRF.start(0)
pwmRR.start(0)
pwmLF.start(0)
pwmLR.start(0)
pwmRF_Reverse.start(0)
pwmRR_Reverse.start(0)
pwmLF_Reverse.start(0)
pwmLR_Reverse.start(0)

def getDistance(direction):
    trig = None
    echo = None
    if direction == 'center':
        trig = dictOut['ultrasound_Center_TRIG']
        echo = dictIn['ultrasound_Center_ECHO']
    elif direction == 'left':
        trig = dictOut['ultrasound_Left_TRIG']
        echo = dictIn['ultrasound_Left_ECHO']
    elif direction == 'right':
        trig = dictOut['ultrasound_Right_TRIG']
        echo = dictIn['ultrasound_Right_ECHO']
    GPIO.output(trig, 0)
    time.sleep(0.01)
    GPIO.output(trig, 1)
    time.sleep(0.00001)
    GPIO.output(trig, 0)
    start = time.time()
    while GPIO.input(echo) == 0:
        start = time.time()
    while GPIO.input(echo) == 1:
        stop = time.time()
    distance = (stop - start) * 34000 / 2
    return distance

def drive(duty):
    setLeftReverse(0)
    setRightReverse(0)
    setLeft(duty)
    setRight(duty)

def reverse(duty):
    setLeft(0)
    setRight(0)
    setLeftReverse(duty)
    setRightReverse(duty)
    
def parking():
    drive(0)
    reverse(0)

def turnRight(duty):
    setRight(0)
    setLeftReverse(0)
    setRightReverse(duty)
    setLeft(duty)

def turnLeft(duty):
    setLeft(0)
    setRightReverse(0)
    setLeftReverse(duty)
    setRight(duty)

# def turnRightReverse():
#     setLeft(0)
#     setLeftReverse(0)
#     setRight(0)
#     setRightReverse(100)
# 
# def turnLeftReverse():
#     setLeft(0)
#     setRightReverse(0)
#     setRight(0)
#     setLeftReverse(100)

def setRight(duty):
    pwmRF.ChangeDutyCycle(duty)
    pwmRR.ChangeDutyCycle(duty)
    
def setLeft(duty):
    pwmLF.ChangeDutyCycle(duty)
    pwmLR.ChangeDutyCycle(duty)

def setRightReverse(duty):
    pwmRF_Reverse.ChangeDutyCycle(duty)
    pwmRR_Reverse.ChangeDutyCycle(duty)

def setLeftReverse(duty):
    pwmLF_Reverse.ChangeDutyCycle(duty)
    pwmLR_Reverse.ChangeDutyCycle(duty)


distSafeForward = 50
distSafeSide = 10

def main():
    try:
        while True:
            distForward = getDistance('center')
            time.sleep(0.02)
            distLeft = getDistance('left')
            time.sleep(0.02)
            distRight = getDistance('right')
            time.sleep(0.02)
            print('forward:{} \t left:{} \t right:{}'.format(distForward, distLeft, distRight))
            if distForward < 15:
                parking()
                print('##### Too close #####')
                if distLeft >= distRight:
                    for i in range(100000):
                        turnLeft(100)
                    print("Turn Left distFoward < 15")
                elif distLeft < distRight:
                    for i in range(100000):
                        turnRight(100)
                    print("Turn RIGHT distFoward < 15")
            elif distForward < distSafeForward and distLeft < distSafeSide and distRight < distSafeSide:
                parking()
                print("Here is not safe")
            elif distForward < distSafeForward and distLeft < distSafeSide and distRight > distSafeSide:
                for i in range(100000):
                    turnRight(100)
                print("Turn RIGHT Code = 1")
            elif distForward < distSafeForward and distLeft > distSafeSide and distRight < distSafeSide:
                for i in range(100000):
                    turnLeft(100)
                print("Turn Left Code = 2")
            elif distForward < distSafeForward and distLeft > distSafeSide and distRight > distSafeSide:
                if distLeft >= distRight:
                    for i in range(100000):
                        turnLeft(100)
                    print("Turn Left Code = 3")
                elif distLeft < distRight:
                    for i in range(100000):
                        turnRight(100)
                    print("Turn RIGHT Code = 4")
            elif distForward > distSafeForward:
                drive(30)
                print('Keep moving')
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
