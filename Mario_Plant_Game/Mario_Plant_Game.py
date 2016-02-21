#!/usr/bin/env python
# Porting from arduino to python
import mraa
from time import sleep
import pyupm_i2clcd as lcd

myLcd = lcd.Jhd1313m1(0, 0x3E, 0x62)

myLcd.clear()
myLcd.setColor(0, 0, 255)
myLcd.setCursor(0,0)

e = mraa.Gpio(5)
s = mraa.Gpio(3)
d = mraa.Gpio(2)
m1 = mraa.Gpio(6)
m2 = mraa.Gpio(4)
t = mraa.Gpio(11)
b = mraa.Gpio(10)

calibrated = False
gameOver = False
stepsMin = 0
stepsMax = 0
curSteps = 0

e.dir(mraa.DIR_OUT)
s.dir(mraa.DIR_OUT)
d.dir(mraa.DIR_OUT)
m1.dir(mraa.DIR_OUT)
m2.dir(mraa.DIR_OUT)
t.dir(mraa.DIR_IN)
b.dir(mraa.DIR_IN)

e.write(0)
d.write(1)
m1.write(0)
m2.write(0)

def setup():

  # Reset stepper motor
  initStepper()


def stepMotor(speed, direction, microStep):
  global curSteps
  if speed == 0:
    return
  stepDirection(direction)
  stepRate(microStep)

  e.write(0)
  s.write(0)
  sleep(0.001)
  s.write(1)
  sleep(0.001)
  e.write(1)
  sleep(speed)

  if direction == 1:
    curSteps+=1
  else: 
    curSteps-=1

def initStepper():
  e.write(1)
  stepDirection(1) # Default to upward direction
  stepRate(3)  # Stepper start at full step

def calibrateStepper():
  global calibrated
  global stepsMax
  global curSteps
  if calibrated == True:
    return

  # Reset to bottom position
  while b.read() == 0:
    stepMotor(0.001, 0, 3)

  curSteps = 0
  while t.read() == 0:
    stepMotor(0.001, 1, 3)
    if curSteps > stepsMax:
      stepsMax = curSteps

  print "Total steps: "+str(stepsMax)
  calibrated = True
  # Reset to bottom position
  while b.read() == 0:
    stepMotor(0.001, 0, 3)

  print "Game Ready!"
  # NOTE: figure this out - should be microseconds?
  sleep(1.5)

def stepDirection(direction):
  if direction == 1:
    d.write(1)
    return 
  elif direction == 0:
    d.write(0)
    return
  else: 
    d.write(1)
    return

def stepRate(microStep):
  if microStep == 3:
    # Full step
    #digitalWrite(ms1Pin, LOW)
    #digitalWrite(ms2Pin, LOW)
    m1.write(0)
    m2.write(0)
    return
  elif microStep == 2:
    # Half step
    #digitalWrite(ms1Pin, HIGH)
    #digitalWrite(ms2Pin, LOW)
    m1.write(1)
    m2.write(0)
    return
  elif microStep == 1:
    # Quarter step
    #digitalWrite(ms1Pin, LOW)
    #digitalWrite(ms2Pin, HIGH)
    m1.write(0)
    m2.write(1)
    return
  elif microStep == 0:
    # Eighth step
    #digitalWrite(ms1Pin, HIGH)
    #digitalWrite(ms2Pin, HIGH)
    m1.write(1)
    m2.write(1)
    return
  else:
    # Full step
    #digitalWrite(ms1Pin, LOW)
    #digitalWrite(ms2Pin, LOW)
    m1.write(0)
    m2.write(0)
    return 

if __name__ == '__main__':
  # Limit switch pins
  topLimitState = 0
  bottomLimitState = 0

  # Motor constants
  speed1 = 1
  speed2 = 500
  speed3 = 750
  speed4 = 1000

  # Calibration values
  stepsMin = 0  # minimum recorded value
  stepsMax = 0  # maximum recorded value
  curSteps = 0
  calibrated = False
  gameOver = False

  setup()
  running = True
  while running:
    topLimitState = t.read()
    bottomLimitState = b.read()
        

    # Calibrate, then move to home
    calibrateStepper()
    print "Calibration Finished"

    #if gameOver == false:
    #  for i in range(0,random(stepsMax / 2, stepsMax)):
    #    stepMotor(random(100, 200), Direction.UP, Microsteps.FULL)
    #  for i in range(0,random(stepsMax / 4, stepsMax / 2)):
    #    stepMotor(random(200, 300), Direction.DOWN, Microsteps.FULL)
    #  for i in range(0, random(stepsMax / 8, stepsMax / 4)):
    #    stepMotor(random(300, 400), Direction.UP, Microsteps.FULL)
   
    print "MOVE UP"
    myLcd.write("MOVE UP")
    d.write(1)
    e.write(0)
    for x in range(0, 1000):
      s.write(1)
      sleep(0.001)
      s.write(0)
      sleep(0.002)

    d.write(0)

    print "MOVE DOWN"
    myLcd.setCursor(0,0)
    myLcd.write("MOVE DOWN")

    for x in range(0, 500):
      s.write(0)
      sleep(0.001)
      s.write(1)
      sleep(0.002)

    e.write(1)

    #gameOver = True
    running = False
    print "Final position: "+str(curSteps)
    # NOTE: May require floating point ? Should test it
    score = (curSteps / stepsMax) * 100.0
    print "You made it "+str(score)+"% to target"
    print "Game Over!"

