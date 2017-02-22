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

def fire_forward():
   motor_a.run_forever(speed_sp=1000)


#==============================================

def fire_backward():
   motor_a.run_forever(speed_sp=-1000)


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
   motor_a.run_forever(speed_sp=0)
#==============================================

def manual():
   speed = 500
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
         fire_forward()
      if k == 'e':
         fire_backward()
      if k == ' ':
         stop()
      if k == 'z':
         exit()
      if k == 'm':
         if speed < 900:
            speed = speed + 100
            print(speed)
         else:
            print("max speed!")
      if k == 'n':
         if speed > 0:
            speed = speed - 100
            print(speed)
         else: print("Speed is Zero!")

#=======================================

def auto():
   #run sweeper
      motor_a.run_forever(speed_sp=900)

   #drive forward
      motor_left.run_to_rel_pos(position_sp=800, speed_sp=500, stop_action="hold")
      motor_right.run_to_rel_pos(position_sp=800, speed_sp=500, stop_action="hold")
      sleep(5)

   #turn left (turn 1)

   #turn right (turn 1)

   #go forward
      motor_left.run_to_rel_pos(position_sp=800, speed_sp=500, stop_action="hold")
      motor_right.run_to_rel_pos(position_sp=800, speed_sp=500, stop_action="hold")
      sleep(5)

   #turn right (turn 2)

   #turn left (turn 2)

   #go forward
      motor_left.run_to_rel_pos(position_sp=800, speed_sp=500, stop_action="hold")
      motor_right.run_to_rel_pos(position_sp=800, speed_sp=500, stop_action="hold")
      sleep(5)

   #turn left (turn 3)

   #go forward (possibly into the wall)
      motor_left.run_to_rel_pos(position_sp=800, speed_sp=500, stop_action="hold")
      motor_right.run_to_rel_pos(position_sp=800, speed_sp=500, stop_action="hold")
      sleep(5)

   #go backwards (if running into the wall)

   #turn left (turn 3)

   #go forward
      motor_left.run_to_rel_pos(position_sp=800, speed_sp=500, stop_action="hold")
      motor_right.run_to_rel_pos(position_sp=800, speed_sp=500, stop_action="hold")
      sleep(5)

   #go forward
      motor_left.run_to_rel_pos(position_sp=800, speed_sp=500, stop_action="hold")
      motor_right.run_to_rel_pos(position_sp=800, speed_sp=500, stop_action="hold")
      sleep(5)

   #turn left (turn 4)
      motor_left.run_to_rel_pos(position_sp=800, speed_sp=500, stop_action="hold")
      motor_right.run_to_rel_pos(position_sp=800, speed_sp=500, stop_action="hold")
      sleep(5)

   #drive forward
      motor_left.run_to_rel_pos(position_sp=800, speed_sp=500, stop_action="hold")
      motor_right.run_to_rel_pos(position_sp=800, speed_sp=500, stop_action="hold")
      sleep(5)

   #get ball

   #turn right (turn 4)

   #go forward
      motor_left.run_to_rel_pos(position_sp=800, speed_sp=500, stop_action="hold")
      motor_right.run_to_rel_pos(position_sp=800, speed_sp=500, stop_action="hold")
      sleep(5)

   #turn right (turn 5)

   #go forward
      motor_left.run_to_rel_pos(position_sp=800, speed_sp=500, stop_action="hold")
      motor_right.run_to_rel_pos(position_sp=800, speed_sp=500, stop_action="hold")
      sleep(5)

   #turn left (turn 6)

   #go forward
      motor_left.run_to_rel_pos(position_sp=800, speed_sp=500, stop_action="hold")
      motor_right.run_to_rel_pos(position_sp=800, speed_sp=500, stop_action="hold")
      sleep(5)

   #turn right (turn 6)

   #go forward
      motor_left.run_to_rel_pos(position_sp=800, speed_sp=500, stop_action="hold")
      motor_right.run_to_rel_pos(position_sp=800, speed_sp=500, stop_action="hold")
      sleep(5)
   #stop sweeper motor
      motor_a.stop()

   exit()

#======================================

def test():
   while True:
      k = getch()
      if k == 't':
         touch1 = TouchSensor('in1')
         print(touch1.value())
      if k == 'c':
         color = ColorSensor('in3')
         color.mode = 'COL-COLOR'
         print(color.value())
      if k == 'z':
         exit()

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






