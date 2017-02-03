#!/usr/bin/env python3
# so that script can be run from Brickman

import termios, tty, sys
from ev3dev.ev3 import *
from time import sleep

# attach large motors to ports B and C, medium motor to port A
motor_left = LargeMotor('outB')
motor_right = LargeMotor('outC')
motor_a = MediumMotor('outA')
speed = 400
#==============================================

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    tty.setcbreak(fd)
    ch = sys.stdin.read(1)
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    
    return ch

#==============================================

def fire_forward(ss):
   motor_a.run_forever(speed_sp= ss)


#==============================================

def fire_backward(ss):
   motor_a.run_forever(speed_sp=-ss)


#==============================================

def forward(speed):
   motor_left.run_forever(speed_sp= speed)
   motor_right.run_forever(speed_sp= speed)
#==============================================

def back(speed):
   motor_left.run_forever(speed_sp= -speed)
   motor_right.run_forever(speed_sp=-speed)

#==============================================

def left(speed):
   motor_left.run_forever(speed_sp=-speed)
   motor_right.run_forever(speed_sp=speed)

#==============================================

def right(speed):
   motor_left.run_forever(speed_sp=speed)
   motor_right.run_forever(speed_sp=-speed)
#===============================================

def jokes(type):
   if type == 's':
      print("Are You Sure You Wish to Self Destruct?")

#==============================================

def stop():
   motor_left.run_forever(speed_sp=0)
   motor_right.run_forever(speed_sp=0)

#==============================================

def stopSweeper():
   motor_a.run_forever(speed_sp=0)

#==============================================
def manual():
   print("Manual Mode Engaged!")
   speed = 500
   ss = 500
   while True:
      k = getch()
      #print(k)
      if k == 'w':
         forward(speed)
      if k == 's':
         back(speed)
      if k == 'a':
         left(speed)
      if k == 'd':
         right(speed)
      if k == 'q':
         fire_forward(ss)
      if k == 'e':
         fire_backward(ss)
      if k == ' ':
         stop()
      if k == 'v':
         stopSweeper()
      if k == 'p':
         Sound.play('sounds/Hey.wav')
      if k == 'z':
         exit()
      if k == 'm':
         if speed < 900:
            speed = speed + 100
            print("Moving Speed is " + str(speed))
         else:
            print("max moving speed!")
      if k == 'n':
         if speed > 0:
            speed = speed - 100
            print("Moving Speed is " + str(speed))
         else: print("Speed is Zero!")
      if k == 'k':
         if ss < 900:
            ss = ss + 100
            print("Sweeper Speed is " + str(ss))
         else:
            print("max sweeper speed!")
      if k == 'j':
         if ss > 0:
            ss = ss - 100
            print("Sweeper Speed is " + str(ss))
         else: print("Speed is Zero!")
      if k == 'b':
         break
   test()

#=======================================
def turnRightAuto(turnDeg):
   gy = GyroSensor('in1')
   #gy.mode = 'GYRO-ANG'
   initialAngle = gy.value()
   finalAngle = initialAngle + turnDeg
   stop()
   while gy.value() < finalAngle:
      right(300)
      motorStates = motor_a.state
      for i in range(len(motorStates)):
         state = motorStates[i]
         if state == 'stalled':
            fire_backward(500)
            sleep(1)
            fire_forward(400)
         else:
            None
      else:
         None
   print("Right Turn Success at " + str(turnDeg) + " degrees")
   stop()
#=======================================
def turnLeftAuto(turnDeg):
   gy = GyroSensor('in1')
   #gy.mode = 'GYRO-ANG'
   initialAngle = gy.value()
   finalAngle = initialAngle - turnDeg
   back(100)
   while gy.value() > finalAngle:
      left(300)
      motorStates = motor_a.state
      for i in range(len(motorStates)):
         state = motorStates[i]
         if state == 'stalled':
            fire_backward(500)
            sleep(1)
            fire_forward(400)
         else:
            None
      else:
         None
   print("Left Turn Success at " + str(turnDeg) + " degrees")
   stop()

#======================================
def checkPath(expectedAngle, actualAngle): #Checks to see if the robot has strayed off path
   if expectedAngle > (actualAngle + 5):
      print('Expected: ' + str(expectedAngle))
      print('Actual: ' + str(actualAngle))
      offset = expectedAngle - actualAngle
      turnRightAuto(offset)
      print('Offset left ' + str(offset))
   elif expectedAngle < (actualAngle -5):
      print('Expected: ' + str(expectedAngle))
      print('Actual: ' + str(actualAngle))
      offset = expectedAngle - actualAngle
      turnLeftAuto(offset)
      print('offset right ' + str(offset))
   else:
      None

#======================================
def auto():
   c = 1
   c2 =0
   ts1 = TouchSensor('in3')
   ts2 = TouchSensor('in4')
   btn = Button()
   us = UltrasonicSensor('in2')
   us.mode = 'US-DIST-CM'
   gy = GyroSensor('in1')
   gy.mode = 'GYRO-ANG'
   initialAngle = gy.value()/10
   expectedAngle = initialAngle
   fire_forward(750)
   while True:
      #checkPath(expectedAngle, (gy.value()/10))
      distance = us.value()/10  # convert mm to cm
      units = us.units
      #print(str(distance) + " " + units)
      c2 += 1
      if c2 == 20:
         c=1
         print('Warning Turn Count Reset!')
      if btn.any():
         stop()
         stopSweeper()
         exit()
      if (((distance > 5) and (distance <20)) and (ts1.value() == 0) and (ts2.value() ==0)):
         forward(400)
         motorStates = motor_a.state
         for i in range(len(motorStates)):
            state = motorStates[i]
            if state == 'stalled':
               fire_backward(500)
               sleep(1)
               fire_forward(400)
            else:
               None
         else:
            None
      else:
         c2 = 0
         if ts1.value() == 1 or ts2.value() == 1:
            back (100)
            sleep(1)
         else:
            None
         forward(400)
         sleep(0.5)
         if c == 1:
            turnRightAuto(10)
            back(100)
            sleep(1)
            expectedAngle += 45
            distance = us.value()/10
            c = 2
         elif c == 2:
            distance = us.value()/10
            print(str(distance) + " " + units)
            turnLeftAuto(20)
            back(100)
            sleep(1)
            expectedAngle -= 90
            c = 3
         elif c == 3:
            distance = us.value()/10
            print(str(distance) + " " + units)
            turnRightAuto(30)
            back(100)
            sleep(1)
            expectedAngle -= 90
            c = 4
         elif c == 4:
            distance = us.value()/10
            print(str(distance) + " " + units)
            turnLeftAuto(40)
            back(100)
            sleep(1)
            expectedAngle -= 90
            c = 5
         elif c == 5:
            distance = us.value()/10
            print(str(distance) + " " + units)
            turnRightAuto(50)
            back(100)
            sleep(1)
            expectedAngle -= 90
            c = 6
         elif c == 6:
            distance = us.value()/10
            print(str(distance) + " " + units)
            turnLeftAuto(60)
            back(100)
            sleep(1)
            expectedAngle -= 90
            c = 7
         elif c == 7:
            distance = us.value()/10
            print(str(distance) + " " + units)
            turnRightAuto(70)
            back(100)
            sleep(1)
            expectedAngle -= 90
            c = 8
         elif c == 8:
            distance = us.value()/10
            print(str(distance) + " " + units)
            turnLeftAuto(80)
            back(100)
            sleep(1)
            expectedAngle -= 90
            c = 9
         elif c == 9:
            distance = us.value()/10
            print(str(distance) + " " + units)
            turnRightAuto(90)
            back(100)
            sleep(1)
            expectedAngle -= 90
            c = 10
         elif c == 10:
            distance = us.value()/10
            print(str(distance) + " " + units)
            turnLeftAuto(100)
            back(100)
            sleep(1)
            expectedAngle -= 90
            c = 11
         elif c == 11:
            distance = us.value()/10
            print(str(distance) + " " + units)
            turnRightAuto(110)
            back(100)
            sleep(1)
            expectedAngle -= 90
            c = 1
         '''elif c == 12:
            distance = us.value()/10
            print(str(distance) + " " + units)
            turnLeftAuto(30)
            back(100)
            sleep(1)
            expectedAngle -= 90
            c = 1'''
      touch1 = TouchSensor('in4')
   exit()

#======================================

def test():
   print("Test Mode Engaged!")
   while True:
      k = getch()
      if k == 't':
         touch1 = TouchSensor('in4')
         print(touch1.value())
      if k == 'c':
         color = ColorSensor('in3')
         color.mode = 'COL-COLOR'
         print(color.value())
      if k =='u':
         us = UltrasonicSensor('in2')
         us.mode = 'US-DIST-CM'
         units = us.units
         distance = us.value()/10  # convert mm to cm
         print(str(distance) + " " + units)
      if k == 'g':
         gy = GyroSensor('in1')
         gy.mode='GYRO-ANG'
         units = gy.units
         angle = gy.value()
         print(str(angle) + " " + units)
      if k == 'b':
         break
      if k == 'm':
         print(motor_a.state)
         motorStates = motor_a.state
         for i in range(len(motorStates)):
            state = motorStates[i]
            if state == 'stalled':
               print('True')
      if k == 'z':
         exit()
   manual()
#======================================

print("Please Select a Mode")
print ("Autonomous (a), Manual (m), or Test (t)")
k = None
Sound.play('sounds/Hey.wav')
while k!='a' and k!='m':
    k = getch()
    if k == 'a':
       auto()
    if k == 'm':
       manual()
    if k == 't':
       test()
    if k == 's':
       jokes('s')
    else:
       print("Please Enter (a) (m) or (t)!")






