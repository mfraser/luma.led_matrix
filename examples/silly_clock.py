#!/usr/bin/env python3
import time
from datetime import datetime

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT


def minute_change(device):
    '''When we reach a minute change, animate it.'''
    hours = datetime.now().strftime('%H')
    minutes = datetime.now().strftime('%M')

    def helper(current_y):
        with canvas(device) as draw:
            text(draw, (0, 1), hours, fill="white", font=proportional(CP437_FONT))
            text(draw, (15, 1), ":", fill="white", font=proportional(TINY_FONT))
            text(draw, (17, current_y), minutes, fill="white", font=proportional(CP437_FONT))
        time.sleep(0.1)
    for current_y in range(1, 9):
        helper(current_y)
    minutes = datetime.now().strftime('%M')
    for current_y in range(9, 1, -1):
        helper(current_y)


def animation(device, from_y, to_y):
    '''Animate the whole thing, moving it into/out of the abyss.'''
    hourstime = datetime.now().strftime('%H')
    mintime = datetime.now().strftime('%M')
    current_y = from_y
    while current_y != to_y:
        with canvas(device) as draw:
            text(draw, (0, current_y), hourstime, fill="white", font=proportional(CP437_FONT))
            text(draw, (15, current_y), ":", fill="white", font=proportional(TINY_FONT))
            text(draw, (17, current_y), mintime, fill="white", font=proportional(CP437_FONT))
        time.sleep(0.1)
        current_y += 1 if to_y > from_y else -1


def main():
    # Setup for Banggood version of 4 x 8x8 LED Matrix (https://bit.ly/2Gywazb)
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=4, block_orientation=90, blocks_arranged_in_reverse_order=True)
    device.contrast(1)

    # The time ascends from the abyss...
    animation(device, 8, 1)

    toggle = False  # Toggle the second indicator every second
    while True:
        toggle = not toggle
        now = datetime.now()
        sec = now.second
        hour = now.hour
        minute =  now.minute
        if sec == 59:
            # When we change minutes, animate the minute change
            minute_change(device)
        elif (hour > 7 and hour < 19) and minute ==0 and sec == 0:
            # Half-way through each minute, display the complete date/time,
            # animating the time display into and out of the abyss.
            full_msg = now.strftime('%a %H.%M %d/%m/%y')
            animation(device, 1, 8)
            show_message(device, full_msg, fill="white", font=proportional(CP437_FONT))
            animation(device, 8, 1)
        else:
            # Do the following twice a second (so the seconds' indicator blips).
            # I'd optimize if I had to - but what's the point?
            # Even my Raspberry PI2 can do this at 4% of a single one of the 4 cores!
            with canvas(device) as draw:
                text(draw, (0, 1), f'{hour:02d}', fill="white", font=proportional(CP437_FONT))
                text(draw, (15, 1), ":" if toggle else " ", fill="white", font=proportional(TINY_FONT))
                text(draw, (17, 1), f'{minute:02d}', fill="white", font=proportional(CP437_FONT))
            time.sleep(0.5)


if __name__ == "__main__":
    main()
