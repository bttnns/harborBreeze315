# harborBreeze315
Controll your Harbor Breeze ceiling fan that comes with a remote using a Raspberry Pi and a FS1000A (315Mhz RF Transmitter)

My main goal is to have a simple API for my Harbor Breeze Ceiling fan to be controlled by [Home Assistant](https://hass.io)

The Remote has a [FCC ID = A25-TX012](https://fcc.io/A25-TX012), DIP Switch under the battery = 1

I'm using the commonly found for cheap [FS1000A Transmitter](https://www.amazon.com/HiLetgo-Transmitter-Receiver-Arduino-Raspberry/dp/B00LNADJS6)

# How to?

## Hardware
Hook up the FS1000A to the Pi's GPIO PINs.

FS1000A:Pi GPIO
- GND:GND
- VCC:5V
- DATA: GPIO 23

## Configurables
Set the configurables at the top of `app.py`.

## Run it
Then run the script to TX the code where `function = variable name of command`

`python3 app.py <function>`

Examples:
- `python3 app.py fs4` set Fan Speed 4, Summer Direction
- `python3 app.py liT` toggle Light ON/OFF
 
