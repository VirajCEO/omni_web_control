import psutil
import os
import sys
import RPi.GPIO as GPIO
import time
from gpiozero import Motor,LED
from time import sleep
from gpiozero import DistanceSensor
import base64

 

in1 = 23
in2 = 24
en = 25
in3 = 17
in4 = 27
en2 = 22
in5 = 16
in6 = 13
en3 = 29

start_speed=80
turn_speed=80
turn_ancle=0.3



name = "Ragas PI"

GPIO.setmode(GPIO.BCM)
GPIO.cleanup()
GPIO.setwarnings(False)

GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)
GPIO.setup(in5, GPIO.OUT)
GPIO.setup(in6, GPIO.OUT)
GPIO.setup(en3,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.setup(en2,GPIO.OUT)

GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
GPIO.output(in3,GPIO.LOW)
GPIO.output(in4,GPIO.LOW)
GPIO.output(in6,GPIO.LOW)
GPIO.output(in5,GPIO.LOW)

p=GPIO.PWM(en,1000)
p1=GPIO.PWM(en2, 1000)
p2=GPIO.PWM(en3, 1000)
p.start(start_speed)
p1.start(start_speed)
p2.start(start_speed)

def CarForward(*args):
    print("forward")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)   
    GPIO.output(in5,GPIO.LOW)
    GPIO.output(in6,GPIO.HIGH)

def CarRight(*args):
    print("right")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.HIGH)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)
    GPIO.output(in5,GPIO.LOW)
    GPIO.output(in6,GPIO.HIGH)
    sleep(turn_ancle)
 

def CarLeft(*args):
    print("left")
    GPIO.output(in1,GPIO.HIGH)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.HIGH)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(in5,GPIO.HIGH)
    GPIO.output(in6,GPIO.LOW)
    sleep(turn_ancle)


def CarBack(*args):
    print("back")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3,GPIO.LOW)
    GPIO.output(in4,GPIO.HIGH)  
    GPIO.output(in5,GPIO.HIGH)
    GPIO.output(in6,GPIO.LOW)

def CarStop(*args):
    print("stop")
    GPIO.output(in1,GPIO.LOW)
    GPIO.output(in2,GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4,GPIO.LOW)
    GPIO.output(in5,GPIO.LOW)
    GPIO.output(in6,GPIO.LOW)

    
def CarSpeed(*args):

    global start_speed
    start_speed=float(args[0])
    print(start_speed)

def setspeed1(speed):
    p.ChangeDutyCycle(speed)


def setspeed2(speed):
    p1.ChangeDutyCycle(speed)
    

def setspeed3(speed):
    p2.ChangeDutyCycle(speed)


def SystemEnd(*args):
    GPIO.cleanup()


def stop():
    CarStop()



