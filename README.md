# lcars-pi-clock
LCARS (Star Trek TNG) themed clock/calendar for WaveShare e-ink or e-paper display on Raspberry Pi

Directory structure:

- project root
  - pic directory
    - Font.ttc
  - lib directory
    - epd library
  - rpi-clock.py
   
I just duplicated the python directory from the WaveShare package:
https://github.com/waveshare/e-Paper/tree/master/RaspberryPi%26JetsonNano/python
- Then I copied rpi-clock.py into that directory
- Then I ran setup.py install to install the library
- Then I copied Font.ttc into the pic directory (Swiss 911 Ultra Compressed font)

The code is currently configured specifically to use the 2.7" e-Paper hat:
https://www.waveshare.com/wiki/2.7inch_e-Paper_HAT

![](lcars-eink-pi-clock.JPG?raw=true)
