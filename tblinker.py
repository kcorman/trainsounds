import RPi.GPIO as GPIO
import time

pwmPin = 18
ledPin = 16

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)
GPIO.setup(12, GPIO.IN)
GPIO.output(ledPin, GPIO.LOW)
print("starting timer")
sleepTime=2.0
timer_on = False
def getSleepTime():
    global sleepTime
    if(sleepTime < .03): return .03
    sleepTime = sleepTime / 1.5
    return sleepTime

def runBlinker():
    while 1:
        st = getSleepTime()
        time.sleep(st)
        GPIO.output(ledPin, GPIO.LOW)
        time.sleep(st)
        GPIO.output(ledPin, GPIO.HIGH)
        i = GPIO.input(12)
        if(i == 2):
            break
ticks = 0
while True:
    i = GPIO.input(12)
    print("input = " + str(i))
    if(i == 1 and not timer_on):
        GPIO.output(ledPin, GPIO.HIGH)
        timer_on = True
        ticks = 20
    if(timer_on):
        ticks-=1
        if(ticks == 0):
            timer_on = False
            GPIO.output(ledPin, GPIO.LOW)

    time.sleep(.1)

def callback(channel):
    print("Detected rise")


"""GPIO.add_event_detect(12, GPIO.RISING, callback=callback, bouncetime=300)

while True:
    time.sleep(1)"""
