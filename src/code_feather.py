import asyncio

import board
import digitalio
import neopixel
from adafruit_debouncer import Button

# Using NeoKey FeatherWing: https://www.adafruit.com/product/4979

pixels = neopixel.NeoPixel(board.D9, 2)
buttons = []
for p in (board.D5, board.D6):
    pin = digitalio.DigitalInOut(p)
    pin.pull = digitalio.Pull.UP
    buttons.append(Button(pin))

pixels.brightness = 0.1
pixels[0] = (0xFF, 0, 0)
pixels[1] = (0, 0, 0xFF)


async def update_buttons() -> None:
    while True:
        for i, b in enumerate(buttons):
            b.update()
            if b.short_count:
                print(f"{i} short count: {b.short_count}")
            if b.long_press:
                print(f"{i} long press")
        await asyncio.sleep(0.0001)


asyncio.run(update_buttons())
