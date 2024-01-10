import time

import board
import digitalio
import usb_hid
from adafruit_macropad import MacroPad

from buttons import *

print("\n")

macropad = MacroPad()
gamepad = usb_hid.devices[0]

REPORT_LENGTH = 9


def led_colors():
    while True:
        yield (0x40, 0x00, 0x00)
        yield (0x40, 0x40, 0x00)
        yield (0x00, 0x40, 0x00)
        yield (0x00, 0x40, 0x40)
        yield (0x00, 0x00, 0x40)
        yield (0x40, 0x00, 0x40)


color = led_colors()
buttons = Buttons()
active = False
while True:
    timescale = 1_000_000_000
    t = (time.monotonic_ns() % timescale) / timescale
    event = macropad.keys.events.get()
    if event:
        if event.pressed:
            active = not active
            print(f"{active=}")
        if active:
            macropad.pixels.fill(next(color))
        else:
            macropad.pixels.fill((0, 0, 0))
    buttons[A] = active * (t < 0.25)
    print(buttons)

    report = bytearray(REPORT_LENGTH)
    report[0:2] = bytes(buttons)
    # print(t)
    # print(buttons)
    # print(f"Sending report: {report.hex(' ')}")
    try:
        gamepad.send_report(report)
    except OSError:
        print("Skipping due to OS error.")
