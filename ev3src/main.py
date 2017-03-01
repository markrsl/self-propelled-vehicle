#!/usr/bin/env python3
# coding = utf-8
'''
Created on 2017/2/24
self-propelled vehicle based on EV3
@author: Mark Hsu
'''
import time
import ev3dev.ev3 as ev3

ev3.Sound.speak("Let's go!")

time.sleep(2)

motorRight = ev3.Motor('outA')
#motorRight.run_timed(time_sp=1000, speed_sp=500)

motorLeft = ev3.Motor('outC')
#motorLeft.run_timed(time_sp=1000, speed_sp=500)

usLeft = ev3.UltrasonicSensor('in4')
usRight = ev3.UltrasonicSensor('in2')
touch = ev3.TouchSensor()
color = ev3.ColorSensor()

#ir =  ev3.InfraredSensor()
#while True:
#    print(ir.proximity)
#    print('Right: {} \t Left: {}'.format(usRight.distance_centimeters, usLeft.distance_centimeters))

def main():
    try:
        while True:
            isTouch = touch.is_pressed
            distLeft = usLeft.distance_centimeters
            distRight = usRight.distance_centimeters
            print('isTouch:{} \t left:{} \t right:{}'.format(isTouch, distLeft, distRight))

            if distLeft < 100:
                speedRight = 300
            elif distLeft > 2000:
                speedRight = 500
            else:
                speedRight = (2*distLeft + 5500) / 19

            if distRight < 100:
                speedLeft = 300
            elif distRight > 2000:
                speedLeft = 500
            else:
                speedLeft = (2*distRight + 5500) / 19

            if isTouch:
                motorLeft.stop()
                motorRight.stop()
                motorLeft.run_timed(time_sp=1000, speed_sp=-1000)
                motorRight.run_timed(time_sp=1000, speed_sp=-1000)
                time.sleep(1)
                motorLeft.stop()
                motorRight.stop()
                if distLeft > distRight:
                    motorLeft.run_timed(time_sp=1500, speed_sp=-110)
                    motorRight.run_timed(time_sp=1500, speed_sp=110)
                else:
                    motorLeft.run_timed(time_sp=1500, speed_sp=110)
                    motorRight.run_timed(time_sp=1500, speed_sp=-110)
                time.sleep(1.5)
            else:
                motorLeft.run_forever(speed_sp = speedLeft)
                motorRight.run_forever(speed_sp = speedRight)

    except KeyboardInterrupt:
        print('Bye')
    finally:
        motorLeft.stop()
        motorRight.stop()

if __name__ == '__main__':
    main()
