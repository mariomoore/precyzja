import RPi.GPIO as GPIO
import time

TRIG = 23
ECHO = 24
REDLED = 16
GREENLED = 20
BLUELED = 21

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

class Czujnik_odleglosci:
    def __init__(self, trig, echo):
        self.TRIG = trig
        self.ECHO = echo
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)

        GPIO.setup(self.TRIG, GPIO.OUT)
        GPIO.setup(self.ECHO, GPIO.IN)

    def pomiar(self):
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)

        while GPIO.input(ECHO)==0:
            pulse_start = time.time()

        while GPIO.input(ECHO)==1:
            pulse_end = time.time()
        
        pulse_duration = pulse_end - pulse_start
        distance = round(pulse_duration * 17150, 2)
        
        return distance
        
    def __del__(self):
        GPIO.cleanup()

class Diody:
    def __init__(self, pinred, pingreen, pinblue):
        self.pinred = pinred
        self.pingreen = pingreen
        self.pinblue = pinblue
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        
        GPIO.setup(self.pinred, GPIO.OUT)
        GPIO.setup(self.pingreen, GPIO.OUT)
        GPIO.setup(self.pinblue, GPIO.OUT)

    def ustaw_diody(self, pin_number):
        if pin_number == self.pinred:
            GPIO.output(self.pinred, GPIO.HIGH)
            GPIO.output(self.pingreen, GPIO.LOW)
            GPIO.output(self.pinblue, GPIO.LOW)
        elif pin_number == self.pinblue:
            GPIO.output(self.pinred, GPIO.LOW)
            GPIO.output(self.pingreen, GPIO.LOW)
            GPIO.output(self.pinblue, GPIO.HIGH)
        else:
            GPIO.output(self.pinred, GPIO.LOW)
            GPIO.output(self.pingreen, GPIO.HIGH)
            GPIO.output(self.pinblue, GPIO.LOW)

    def __del__(self):
        GPIO.cleanup()

if __name__ == "__main__":
    print("Przerwanie pomiaru za pomocą Ctrl+C")
    
    co = Czujnik_odleglosci(TRIG, ECHO)
    d = Diody(REDLED, GREENLED, BLUELED)
    """GPIO.setup(REDLED, GPIO.OUT)
    GPIO.setup(GREENLED, GPIO.OUT)
    GPIO.setup(BLUELED, GPIO.OUT)"""
    
    try:
        while True:
            dystans = co.pomiar()
            if dystans < 10.0:
                d.ustaw_diody(REDLED)
            elif dystans > 30.0:
                d.ustaw_diody(BLUELED)
            else:
                d.ustaw_diody(GREENLED)
            print("Distance:", dystans, "cm")
            time.sleep(1)
    except KeyboardInterrupt:
        print(" Przerwano")
        GPIO.cleanup()