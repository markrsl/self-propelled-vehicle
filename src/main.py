import time
from vehicle import vehicle

def run(flag):
    dSafeForward = 50
    dSafeSide = 10
    try:
#         for i in range(31000):
#             right4WD()
        while flag:
            dforward = vehicle.ultrasound(vehicle.ultrasound_Forward_TRIG, vehicle.ultrasound_Forward_ECHO)
            dLeft = vehicle.ultrasound(vehicle.ultrasound_Left_TRIG, vehicle.ultrasound_Left_ECHO)
            dRight = vehicle.ultrasound(vehicle.ultrasound_Right_TRIG, vehicle.ultrasound_Right_ECHO)
            print('forward:{} \t left:{} \t right:{}'.format(dforward, dLeft, dRight))
             
            if dforward < dSafeForward and dLeft < dSafeSide and dRight < dSafeSide:
                vehicle.stop()
                print("Here is not safe!!!")
            elif dforward < dSafeForward and dLeft < dSafeSide and dRight > dSafeSide:
                vehicle.stop()
                time.sleep(0.5)
                for i in range(31000):
                    vehicle.right4WD()
                print("Turn RIGHT!!!")
            elif dforward < dSafeForward and dLeft > dSafeSide and dRight < dSafeSide:
                vehicle.stop()
                time.sleep(0.5)
                for i in range(31000):
                    vehicle.left4WD()
                print("Turn Left!!!")
            elif dforward < dSafeForward and dLeft > dSafeSide and dRight > dSafeSide:
                vehicle.stop()
                time.sleep(0.5)         
                if dLeft >= dRight:
                    for i in range(31000):
                        vehicle.left4WD()
                    print("Turn Left!!!")
                elif dLeft < dRight:
                    for i in range(31000):
                        vehicle.right4WD()
                    print("Turn RIGHT!!!")
            elif dforward > dSafeForward:
                vehicle.forward()
                print('Keep moving!')
    except KeyboardInterrupt:
        print('Bye')
    finally:
        vehicle.stop()
        vehicle.exit()
        