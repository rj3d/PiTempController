import RPi.GPIO as GPIO
import time

pins = [11, 12, 15]

GPIO.setmode(GPIO.BOARD)

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, False)

