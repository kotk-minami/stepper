from time import sleep
import board
import neopixel

led_count = 3

ORDER = neopixel.GRB

pixel = neopixel.NeoPixel(board.D18, led_count, brightness=0.5, auto_write=False, pixel_order=ORDER)

pixel.fill((0, 200, 0))
pixel.show()
sleep(5)