import time

try:
    from typing import Generator
except ImportError:
    pass
import usb_hid
from adafruit_macropad import MacroPad

from bitfield import Bitfield

print("\n")

macropad = MacroPad()
gamepad = usb_hid.devices[0]

REPORT_LENGTH = 9

Y = 0
B = 1
A = 2
X = 3
L = 4
R = 5
ZL = 6
ZR = 7
Minus = 8
Plus = 9
LS = 10
RS = 11


def led_colors() -> Generator[tuple[int, int, int], None, None]:
    while True:
        yield (0x40, 0x00, 0x00)
        yield (0x40, 0x40, 0x00)
        yield (0x00, 0x40, 0x00)
        yield (0x00, 0x40, 0x40)
        yield (0x00, 0x00, 0x40)
        yield (0x40, 0x00, 0x40)


color = led_colors()
buttons = Bitfield(16)
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
