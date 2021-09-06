import RPi.GPIO as GPIO
import time
import subprocess
import pygame
import sched

pygame.init()
chugs = []
chugs.append(pygame.mixer.Sound("/home/pi/stuff/sounds/ChugSounds/goodchug1.wav"))
chugs.append(pygame.mixer.Sound("/home/pi/stuff/sounds/ChugSounds/goodchug2.wav"))
chugs.append(pygame.mixer.Sound("/home/pi/stuff/sounds/ChugSounds/goodchug3.wav"))
chugs.append(pygame.mixer.Sound("/home/pi/stuff/sounds/ChugSounds/goodchug4.wav"))

idle_sounds = []
idle_sounds.append(pygame.mixer.Sound("/home/pi/stuff/sounds/IdleSounds/LocomotiveIdle1.wav"))
idle_sounds.append(pygame.mixer.Sound("/home/pi/stuff/sounds/IdleSounds/LocomotiveIdle2.wav"))
idle_sounds.append(pygame.mixer.Sound("/home/pi/stuff/sounds/IdleSounds/LocomotiveIdle3.wav"))
idle_sounds.append(pygame.mixer.Sound("/home/pi/stuff/sounds/IdleSounds/LocomotiveIdle4.wav"))
idle_sounds.append(pygame.mixer.Sound("/home/pi/stuff/sounds/IdleSounds/LocomotiveIdle5.wav"))

CHUG_SENSOR=4
chugcounter=0
SECONDS_BEFORE_IDLE_SOUND=5

GPIO.setmode(GPIO.BCM)
GPIO.setup(CHUG_SENSOR, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
scheduler = sched.scheduler(time.time, time.sleep)
last_sound_played_at = None
reset_chug_sound = True
last_real_chug_count = 0
idle_sound_index = 0

# The currently playing idle sound
idle_sound = None
idle_sound_ends_at = None

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

def playIdleSound():
    global last_sound_played_at
    global idle_sound
    global idle_sound_index
    global idle_sound_ends_at
    global scheduler
    print("Checking if should play idle sound")
    now = time.time()
    last = 0.0
    if(last_sound_played_at != None):
        last = last_sound_played_at
    diff = now - last
    if(diff > SECONDS_BEFORE_IDLE_SOUND):
        # It has been more than 5 seconds since last chug, start idle sounds
        if(idle_sound == None or idle_sound_ends_at < now):
            idle_sound = idle_sounds[idle_sound_index]
            idle_sound.play()
            idle_sound_ends_at = now + idle_sound.get_length()
            idle_sound_index = (idle_sound_index + 1) % len(idle_sounds)
            scheduler.enter(idle_sound.get_length(),2, playIdleSound)
        else:
            scheduler.enter(1.0,2,playIdleSound)
    else:
        scheduler.enter(1.0,2,playIdleSound)
    print("End check for idle sound")


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
    if(idle_sound != None and idle_sound_ends_at > time.time()):
        idle_sound.fadeout(2000)
    chugcounter = (chugcounter + 1) % len(chugs)
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
            print("Scheduling chugs")
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

playIdleSound()

try:
    while(True):
        #print("Scheduler run")
        scheduler.run(blocking=False)
        time.sleep(.1)

except KeyboardInterrupt:
    print("Cleaning up")
    GPIO.cleanup()

"""GPIO.add_event_detect(12, GPIO.RISING, callback=callback, bouncetime=300)

while True:
    time.sleep(1)"""
