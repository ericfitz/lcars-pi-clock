#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging

logging.basicConfig(level=logging.DEBUG)

basepath = os.path.dirname(os.path.realpath(__file__))
logging.debug("base path: %s", basepath)

picdir = os.path.join(basepath, 'pic')
logging.debug("picdir: %s", picdir)
libdir = os.path.join(basepath, 'lib')
logging.debug("libdir: %s", libdir)
if os.path.exists(libdir):
    sys.path.append(libdir)

from waveshare_epd import epd2in7      # 2in7 = 1bit; 2in7b = blk/red or 4gray
import time
from PIL import Image,ImageDraw,ImageFont
import traceback

try:

    logging.info("Raspberry Pi LCARS clock for 2.7in WaveShare e-Ink Display")
    epd = epd2in7.EPD()
    logging.debug("Width = %s, Height = %s", format(epd.width), format(epd.height))

    white = 255
    black = 0

    logging.debug("Initialize and clear the display")
    epd.init()
    epd.Clear(white)

    logging.debug("Loading Fonts")
    fontOswald_36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36, 0)
    fontSwiss911_36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36, 1)
    fontSwiss911_24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24, 1)
    fontSwiss911_18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18, 1)
    fontSwiss911_12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12, 1)
    fontFutura_12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12, 2)

# Horizontal orientation
    logging.debug("Setting horizontal orientation")
    HImage = Image.new('1', (epd.height, epd.width), white )  # mode 1 = 1bit, L = 8-bit gray
    drawImage = ImageDraw.Draw(HImage)

# LCARS graphics
    # top graphics
    drawImage.rectangle((0, 0, 35, 15), fill = black )    # vertical bar top segment
    drawImage.rectangle((0, 18, 35, 33), fill = black )    # vertical bar segment 2
    drawImage.text((15, 3), "TIME", font = fontFutura_12, fill = white )
    drawImage.rectangle((0, 36, 35, 51), fill = black )    # vertical bar segment 3
    drawImage.text((15, 21), "DATE", font = fontFutura_12, fill = white )
    drawImage.ellipse((0, 48, 35, 60), fill = black )    # bottom outside corner
    drawImage.rectangle((18, 51, 130, 60), fill = black )    # horiz bar segment 1
    drawImage.text((53, 50), "TIME", font = fontFutura_12, fill = white )
    drawImage.rectangle((133, 51, 245 , 60), fill = black )    # horiz bar segment 2
    drawImage.text((143, 50), "DATE", font = fontFutura_12, fill = white )
    drawImage.ellipse((epd.height-10, 52, epd.height, 60), fill = black )    # horiz bar endcap
    drawImage.rectangle((248, 51, epd.height-6, 60), fill = black )    # horiz bar segment 3
    epd.display(epd.getbuffer(HImage))

    # bottom graphics
    drawImage.ellipse((0, 65, 35, 74), fill = black )    # top outside corner
    drawImage.rectangle((18, 65, epd.height-6, 74), fill = black )    # horizontal bar
    drawImage.ellipse((epd.height-10, 66, epd.height, 74), fill = black)    # end cap for horizontal bar
    drawImage.text((53, 64), "CALENDAR", font = fontFutura_12, fill = white )    # Horizontal bar label
    drawImage.rectangle((0, 71, 35, epd.width), fill = black ) # vertical bar
    epd.display(epd.getbuffer(HImage))

#start the main infinite loop here
# Time computations
    now = time.localtime(time.time())
# put a (if now.minute = oldnow.minute) loop here that sleeps for 1 second
    fmttime = time.strftime("%I:%M", now)
    fmtampm = time.strftime("%p", now)
    fmtdate = time.strftime("%a %b %d", now)
    drawImage.text((50, 5), fmttime, font = fontSwiss911_36, fill = black)
    drawImage.text((108, 10), fmtampm, font = fontSwiss911_18, fill = black)
    drawImage.text((140, 5), fmtdate, font = fontSwiss911_36, fill = black)
    epd.display(epd.getbuffer(HImage))
# end the main loop here

    logging.debug("Clear and sleep")
#    epd.Clear(white)
    epd.sleep()

    epd.Dev_exit()

except IOError as e:
    logging.info(e)

except KeyboardInterrupt:
    logging.debug("ctrl + c:")
    epd2in7.epdconfig.module_exit()
    exit()
