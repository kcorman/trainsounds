import RPi.GPIO as GPIO
import time
import subprocess
import pygame
import sched

pygame.init()
chugs = []
chugs.append(pygame.mixer.Sound("sounds/goodchug1.wav"))
chugs.append(pygame.mixer.Sound("sounds/goodchug2.wav"))

CHUG_SENSOR=26
chugcounter=0

GPIO.setmode(GPIO.BCM)
GPIO.setup(CHUG_SENSOR, GPIO.IN)
scheduler = sched.scheduler(time.time, time.sleep)
last_sound_played_at = None
reset_chug_sound = True
last_real_chug_count = 0

def main():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(CHUG_SENSOR, GPIO.IN)
    readHigh=False
    while True:
        i = GPIO.input(CHUG_SENSOR)
        #print("input = " + str(i))
        if(i == 1):
            if(not readHigh):
                playChug()
            readHigh = True
        elif(i == 0):
            readHigh=False

        time.sleep(.005)

def justPlay():
    while(True):
        playChug()
        time.sleep(.2)

def playSound(i):
    chugs[i].play()
    #return subprocess.Popen(["play", "-q", filename, "bass", "+30"])
    #return subprocess.Popen(["play", "-q", filename])

def playChug(isSource, expected_last_real_chug_count):
    global chugcounter
    global last_sound_played_at
    if(expected_last_real_chug_count != last_real_chug_count):
        return
    print("PlayChug source=" + str(isSource))
    chugcounter = (chugcounter + 1) % 2
    val = chugcounter
    playSound(val)
    if(isSource):
        last_sound_played_at = time.time()

    #return playSound("chug" + str(val) + ".wav")

def scheduleSecondaryChugs():
    global last_sound_played_at
    global last_real_chug_count
    if(last_sound_played_at != None):
        timeDiff = (time.time() - last_sound_played_at)
        scheduler.enter(timeDiff / 3,1, playChug, (False,last_real_chug_count))
        scheduler.enter(2 * timeDiff / 3,1, playChug, (False,last_real_chug_count))

def playChugEvent(ignored):
    global reset_chug_sound
    global last_real_chug_count
    if GPIO.input(CHUG_SENSOR): 
        print("Detected rising edge")
        if(reset_chug_sound == True or reset_chug_sound == False):
            last_real_chug_count +=1
            scheduler.enter(0, 1, playChug, (True,last_real_chug_count))
            scheduleSecondaryChugs()
            reset_chug_sound = False
    else:
        reset_chug_sound = True

def callback(channel):
    print("Detected rise")

#main()
#justPlay()

GPIO.add_event_detect(CHUG_SENSOR, GPIO.BOTH, callback=playChugEvent, bouncetime=20)

try:
    while(True):
        scheduler.run()
        time.sleep(.05)

except KeyboardInterrupt:
    print("Cleaning up")
    GPIO.cleanup()

"""GPIO.add_event_detect(12, GPIO.RISING, callback=callback, bouncetime=300)

while True:
    time.sleep(1)"""
