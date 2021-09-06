import RPi.GPIO as GPIO
import time
import subprocess

CHUG_SENSOR=26
chugcounter=0

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CHUG_SENSOR, GPIO.OUT)
    readHigh=False
    while True:
        i = GPIO.input(CHUG_SENSOR)
        print("input = " + str(i))
        if(i == 1):
            if(not readHigh):
                playChug()
            readHigh = True
        elif(i == 0):
            readHigh=False

        time.sleep(.1)

def justPlay():
    while(True):
        playChug()
        time.sleep(.1)

def playSound(filename):
    #return subprocess.Popen(["play", "-q", filename, "bass", "+30"])
    return subprocess.Popen(["play", "-q", filename])

def playChug():
    global chugcounter
    chugcounter = (chugcounter + 1) % 2
    val = 1 + chugcounter
    return playSound("sounds/goodchug" + str(val) + ".wav")

def callback(channel):
    print("Detected rise")

#main()

justPlay()

"""GPIO.add_event_detect(12, GPIO.RISING, callback=callback, bouncetime=300)

while True:
    time.sleep(1)"""
