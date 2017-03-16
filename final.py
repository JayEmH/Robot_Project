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
      right(200)
      motorStates = motor_a.state
      for i in range(len(motorStates)):
         state = motorStates[i]
         if state == 'stalled':
            fire_backward(1000)
            sleep(.25)
            fire_forward(1000)
            back(300)
            sleep(2)
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
      left(200)
      motorStates = motor_a.state
      for i in range(len(motorStates)):
         state = motorStates[i]
         if state == 'stalled':
            fire_backward(1000)
            sleep(.25)
            fire_forward(1000)
            back(300)
            sleep(2)
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
   print("Gyroscope Calibration in Progress...")
   c = 1
   c2 =0
   ts1 = TouchSensor('in3')
   ts2 = TouchSensor('in4')
   btn = Button()
   us = UltrasonicSensor('in2')
   us.mode = 'US-DIST-CM'
   gy = GyroSensor('in1')
   gy.mode = 'GYRO-ANG'
   sleep(3)
   gy.mode = 'GYRO-RATE'
   sleep(3)
   gy.mode = 'GYRO-ANG'
   sleep(3)
   #gy.mode = 'GYRO-ANG'
   initialAngle = gy.value()/10
   expectedAngle = initialAngle
   fire_forward(750)
   # Main drive
   forward(200)
   k = getch()
   distance = us.value() / 10  # convert mm to cm
   # Begin Changes
   # Elements in turnList: (Direction, degrees, time reverse, time forward)
   # Forward occurs PRIOR to turn
   # Reverse Occurs AFTER Turn and initiates next turn (does not wait on us sensor)
   # Direction input as 'R' or 'L' (Right or Left)
   print("Select Task: P6 (6) or P4/5 (5)")
   while k != '6' and k != '5':
      k = getch()

   if k == '5':
      turnList = [('L', 70, 0, 0), ('R', 45, 0, 1), ('R', 25, 0, 0), ('R', 50, 2.1, 0.1), ('R', 40, 2, 0), ('R', 10, 1, 2), ('R', 10, 2, 1), ('L', 20, 0, 0)]
   elif k == '6':
      turnList = [('L', 70, 0, .5),('R', 300, 0, 3),('R', 300, 0, 1)]

   for i in range(len(turnList)):
       if k == '6':
         distance = 255
       while distance != 255 and ts1.value() == 0 and ts2.value() == 0:
           distance = us.value() / 10
       distance = 0
       turn = turnList[i]
       forward(200)
       sleep(turn[3])
       if turn[0] == 'L':
           turnLeftAuto(turn[1])
       else:
           turnRightAuto(turn[1])
       back(500)
       sleep(turn[2])
       if turn[2] != 0:
           distance = 255
       forward(200)
   while True:
      '''k = getch()
      if k == 'b':
         stop()
         stopSweeper()
         exit()
      else:
         None'''
      #checkPath(expectedAngle, (gy.value()/10))
      distance = us.value()/10  # convert mm to cm
      units = us.units
      print(str(distance) + " " + units)
      if ts1.value == 1 or ts2.value == 2:
         print("Touch Sensor Triggered")
      c2 += 1
      if c2 == 45:
         c=1
         print('Warning Turn Count Reset!')
      if btn.any():
         stop()
         stopSweeper()
         exit()
      if ((distance) > 0 and (distance < 5)):
            print('DANGER Golf ball detected')
            forward(600)
            sleep(4.5)
            #c = 1
      if ((distance > 60) and (distance < 100)):
         turnLeftAuto (20)
         back (300)
         sleep(4)
         turnLeftAuto(80)
         c = 1
      if (((distance > 0) and (distance <20)) and (ts1.value() == 0) and (ts2.value() ==0)):
         forward(200) # 4 and 20
         motorStates = motor_a.state
         for i in range(len(motorStates)):
            state = motorStates[i]
            if state == 'stalled':
               fire_backward(500)
               sleep(.5)
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
         turnDeg = c * 10
         if c % 2 == 0:
             turnLeftAuto(turnDeg)
         else:
             turnRightAuto(turnDeg)
         back(100)
         sleep(1)
         c += 1
   exit()

#======================================

def test():
   print("Test Mode Engaged!")
   while True:
      k = getch()
      if k == 't':
         touch1 = TouchSensor('in4')
         print(touch1.value())
      if k == 'r':
         turnRightAuto(90)
         k = None
      if k == 'l':
         turnLeftAuto(90)
         k = None
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
         print(motor_left.state)
         motorStates = motor_left.state
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






