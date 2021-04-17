#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.

import sys
import time
from datetime import datetime

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.virtual import viewport, sevensegment

serial = spi(port=0, device=0, gpio=noop())
device = max7219(serial, cascaded=1)
seg = sevensegment(device)

device.contrast(0x20)

def main():
    while 1:
        now = datetime.now()
        APM = now.strftime("%p")[0:1]
        if int(now.strftime("%S"))%2 ==0:
            seg.text = now.strftime("%I-%M")+"  "+APM
        else:
            seg.text = now.strftime("%I %M")+"  "+APM
        time.sleep(0.5)

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nExiting by user request.\n', file=sys.stderr)
        sys.exit(0)
