import time
import sys
import RPi.GPIO as GPIO

f1 = '0011000011111110101110010'
f2 = '0011000011111110110110010'
f3 = '0011000011111110100110010'
f4 = ''
f5 = ''
f6 = ''

short_delay = 0.00038
long_delay = 0.00077
extended_delay = 0.008
NUM_ATTEMPTS = 4
TRANSMIT_PIN = 23

def transmit_code(code):
    '''Transmit a chosen code string using the GPIO transmitter'''
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRANSMIT_PIN, GPIO.OUT)
    for t in range(NUM_ATTEMPTS):
        for i in code:
            if i == '1':
                time.sleep(short_delay)
                GPIO.output(TRANSMIT_PIN, 1) 
                time.sleep(long_delay)
                GPIO.output(TRANSMIT_PIN, 0)
            elif i == '0':
                time.sleep(long_delay)
                GPIO.output(TRANSMIT_PIN, 1)
                time.sleep(short_delay)
                GPIO.output(TRANSMIT_PIN, 0)
            else:
                continue
        GPIO.output(TRANSMIT_PIN, 0)
        time.sleep(extended_delay)
    GPIO.cleanup()

if __name__ == '__main__':
    for argument in sys.argv[1:]:
        exec('transmit_code(' + str(argument) + ')')

