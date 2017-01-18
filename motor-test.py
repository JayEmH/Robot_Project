#!/usr/bin/env python3
# so that script can be run from Brickman

import termios, tty, sys
from ev3dev.ev3 import *

# attach large motors to ports B and C, medium motor to port A
motor_left = LargeMotor('outB')
motor_right = LargeMotor('outC')
motor_a = MediumMotor('outA')
print("running")
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
   motor_a.run_forever(speed_sp=150)


#==============================================

def fire_backward():
   motor_a.run_forever(speed_sp=-150)


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

#==============================================

def stop():
   motor_left.run_forever(speed_sp=0)
   motor_right.run_forever(speed_sp=0)
   motor_a.run_forever(speed_sp=0)
#==============================================
speed = 400
while True:
   k = getch()
   print(k)
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
