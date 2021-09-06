import RPi.GPIO as GPIO
import time

pwmPin = 18
ledPin = 12

GPIO.setmode(GPIO.BCM)
GPIO.setup(ledPin, GPIO.OUT)
#GPIO.setup(12, GPIO.IN)
GPIO.output(ledPin, GPIO.LOW)
print("starting timer")
sleepTime=2.0
def getSleepTime():
    global sleepTime
    if(sleepTime < .03): return .03
    sleepTime = sleepTime / 1.5
    return sleepTime

def runBlinker():
    while 1:
        st = getSleepTime()
        time.sleep(st)
        print("set mode low")
        GPIO.output(ledPin, GPIO.LOW)
        time.sleep(st)
        print("set mode high")
        GPIO.output(ledPin, GPIO.HIGH)

while True:
    runBlinker()

def callback(channel):
    print("Detected rise")


"""GPIO.add_event_detect(12, GPIO.RISING, callback=callback, bouncetime=300)

while True:
    time.sleep(1)"""
