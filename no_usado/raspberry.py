#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
from demo_opts import get_device
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT,TINY_FONT, LCD_FONT
from luma.core.virtual import viewport
from itertools import repeat
# from luma.core.interface.serial import spi, noop
# from luma.led_matrix.device import max7219

def main():
    #serial = spi(port=0, device=0, gpio=noop())
    #device = max7219(serial, cascaded=2,block_orientation=-90)
    device = get_device()
    msg = "Aguante Python y la UNLP 2k19"
    print(msg)
    show_message(device, msg, fill='red', font=proportional(LCD_FONT), scroll_delay=0.05)
    
#    for _ in repeat(None):
#        time.sleep(1)
#        msg = time.asctime()
#        msg = time.strftime("%S")
#        
#        with canvas(device) as draw:
#        # draw.rectangle(device.bounding_box, outline="white", fill="black")
#            text(draw, (1, 0), msg, fill="white")
#    time.sleep(2)
#    pass
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
