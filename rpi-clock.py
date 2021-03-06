#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
import logging
import calendar

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

def minutechanged(oldminute):
    currentminute = time.localtime()[4]

    if ((currentminute - oldminute) >= 1) or (oldminute == 59 and currentminute == 0):
        return True
    else:
        return False

def monthchanged(oldtime):
    currentyear = time.localtime()[0]
    currentmonth = time.localtime()[1]
    oldyear = oldtime[0]
    oldmonth = oldtime[1]

    if ((currentmonth != oldmonth) or (currentyear != oldyear)):
        return True
    else:
        return False

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
    fontSwiss911_36 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 36, 0)
    fontSwiss911_24 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 24, 0)
    fontSwiss911_18 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 18, 0)
    fontSwiss911_12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12, 0)
    fontFixedWidth_12 = ImageFont.truetype(os.path.join(picdir, 'Font.ttc'), 12, 1)

# Horizontal orientation
    logging.debug("Setting horizontal orientation")
    HImage = Image.new('1', (epd.height, epd.width), white )  # mode 1 = 1bit, L = 8-bit gray
    drawImage = ImageDraw.Draw(HImage)

# LCARS graphics
    # top graphics
    drawImage.rectangle((0, 0, 35, 15), fill = black )    # vertical bar top segment
    drawImage.rectangle((0, 18, 35, 33), fill = black )    # vertical bar segment 2
    #drawImage.text((15, 3), "TIME", font = fontFixedWidth_12, fill = white )
    drawImage.rectangle((0, 36, 35, 51), fill = black )    # vertical bar segment 3
    #drawImage.text((15, 21), "DATE", font = fontFixedWidth_12, fill = white )
    drawImage.ellipse((0, 48, 35, 60), fill = black )    # bottom outside corner
    drawImage.rectangle((18, 51, 130, 60), fill = black )    # horiz bar segment 1
    drawImage.text((53, 51), "TIME", font = fontFixedWidth_12, fill = white )
    drawImage.rectangle((133, 51, 245, 60), fill = black )    # horiz bar segment 2
    drawImage.text((143, 51), "DATE", font = fontFixedWidth_12, fill = white )
    drawImage.ellipse((epd.height-10, 52, epd.height, 60), fill = black )    # horiz bar endcap
    drawImage.rectangle((248, 51, epd.height-6, 60), fill = black )    # horiz bar segment 3
#    epd.display(epd.getbuffer(HImage))

    # bottom graphics
    drawImage.ellipse((0, 65, 35, 74), fill = black )    # top outside corner
    drawImage.rectangle((18, 65, 245, 74), fill = black )    # horizontal bar 1
    drawImage.rectangle((248, 65, epd.height-6, 74), fill = black )    # horizontal bar 2
    drawImage.ellipse((epd.height-10, 66, epd.height, 74), fill = black)    # end cap for horizontal bar
    drawImage.text((53, 65), "CALENDAR", font = fontFixedWidth_12, fill = white )    # Horizontal bar label
    drawImage.rectangle((0, 71, 35, epd.width), fill = black ) # vertical bar
    epd.display(epd.getbuffer(HImage))

    now = time.localtime(0)

    while True:
        last = now
        now = time.localtime()
        if minutechanged(last[4]):
            fmttime = time.strftime("%I:%M", now)
            fmtampm = time.strftime("%p", now)
            fmtdate = time.strftime("%a %b %d", now)
            drawImage.rectangle((36, 0, epd.height, 50), fill = white )
            drawImage.text((50, 5), fmttime, font = fontSwiss911_36, fill = black)
            drawImage.text((108, 10), fmtampm, font = fontSwiss911_18, fill = black)
            drawImage.text((140, 5), fmtdate, font = fontSwiss911_36, fill = black)
            if monthchanged(last):
                drawImage.rectangle((36, 75, epd.height, epd.width), fill = white )
                c = calendar.TextCalendar(calendar.SUNDAY)
                logging.debug("Now[0] = %s, Now[1] %s", now[0], now[1])
                strcal = c.formatmonth( now[0], now[1] )
                logging.debug("%s", strcal)
                drawImage.text((50, 80), strcal, font = fontFixedWidth_12, spacing = 3, fill = black )
            epd.display(epd.getbuffer(HImage))
        else:
            time.sleep(1)

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
