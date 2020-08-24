from flask import Flask
from flask import request
import time
import sys
import RPi.GPIO as GPIO

app = Flask(__name__)

# Configurables
NUM_ATTEMPTS = 6 # How many times to repeat the code
TRANSMIT_PIN = 23 # GPIO Pin for FS1000A Data
DIP = 1 # Remote DIP Switch: 0 or 1

# Delays for keying, should not need to change these
short_delay = 0.00038
long_delay = 0.00077
extended_delay = 0.008

# Harbor breeze remote bits See the manual for the button # mapping
# https://fccid.io/A25-TX012/User-Manual/User-manual-1937614

# Preambles depending on remote DIP position. Code = dpX + func
dp0 = '00000000000000000' # Dip Switch 0 Preamble
dp1 = '00110000111111101' # Dip Switch 1 Preamble

# Fan button functions. Button #1 in user manual
# Winter (Counterclockwise)
fw1 = '01110010' # Fan Speed 1
fw2 = '10110010' # Fan Speed 2
fw3 = '00110010' # Fan Speed 3
fw4 = '11010010' # Fan Speed 4
fw5 = '01010010' # Fan Speed 5
fw6 = '10010010' # Fan Speed 6
fwT = '11110010' #2 Fan ON/OFF
fwN = '00010010' #3 Nature Breeze

# Summer (Clockwise)
fs1 = '01111010' # Fan Speed 1
fs2 = '10111010' # Fan Speed 2
fs3 = '00111010' # Fan Speed 3
fs4 = '11011010' # Fan Speed 4
fs5 = '01011010' # Fan Speed 5
fs6 = '10011010' # Fan Speed 6
fsT = '11111010' #2 Fan ON/OFF
fsN = '00011010' #3 Nature Breeze

# Fan Direction
fwD = '11100010' #8 Fan Winter Direction
fsD = '11101010' #8 Fan Summer Direction

# Light button mappings
liH = '00001110' #4 Home Shield (Lights cycle on for 5-20 minutes and off for 60 minutes, simulating occupancy)
liT = '01101010' #5 Light ON/OFF
liD = '10101010' #5 Light DIMMING

# Delay button mappings
deO = '00100010' #6 Delay Off
de2 = '01101110' #7 Delay 2H
de4 = '10101110' #7 Delay 4H
de8 = '00101110' #8 Delay 8H


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

@app.route('/hb/<code>', methods = ['GET', 'POST'])
def hb(code):
    if request.method == 'GET':
        """return the information for <user_id>"""
        return "yes"
    if request.method == 'POST':
        """modify/update the information for <user_id>"""
        # you can use <user_id>, which is a str but could
        # changed to be int or whatever you want, along
        # with your lxml knowledge to make the required
        # changes
        data = request.form # a multidict containing POST data
        print(data)
        return "ok"

if __name__ == "__main__":
    app.run(host='0.0.0.0')

#if __name__ == '__main__':
    #for argument in sys.argv[1:]:
        #if DIP == 0:
            #exec('transmit_code(dp0 + ' + str(argument) + ')')
        #elif DIP == 1:
            #exec('transmit_code(dp1 + ' + str(argument) + ')')
