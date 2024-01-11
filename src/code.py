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

# Buttons
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

# HAT switch directions
HAT_N = 0
HAT_NE = 1
HAT_E = 2
HAT_SE = 3
HAT_S = 4
HAT_SW = 5
HAT_W = 6
HAT_NW = 7
HAT_CENTER = 8


def map_analog_value(value: float) -> int:
    """Maps analog values [-1.0, 1.0] to integer range [0, 255]."""
    # TODO(dhrosa): 0.0 should map to 128, not 127
    value = max(value, -1.0)
    value = min(value, 1.0)
    return int((value + 1) * 255 / 2)


class Report:
    """High-level HID report payload wrapper"""

    def __init__(self) -> None:
        # 16-bit (2 bytes) button bitfield
        self.buttons = Bitfield(16)
        # 4-bit (1 byte) HAT switch state
        self.hat = HAT_CENTER
        # 4x 8-bit (1 byte) analog stick state
        self.lx = 0
        self.ly = 0
        self.rx = 0
        self.ry = 0

    def __bytes__(self) -> bytes:
        """Convert to raw bytes payload for HID report."""
        vendor_specific = 0
        return bytes(self.buttons) + bytes(
            (
                self.hat,
                map_analog_value(self.lx),
                map_analog_value(self.ly),
                map_analog_value(self.rx),
                map_analog_value(self.ry),
                vendor_specific,
                vendor_specific,
            )
        )


def led_colors() -> Generator[tuple[int, int, int], None, None]:
    while True:
        yield (0x40, 0x00, 0x00)
        yield (0x40, 0x40, 0x00)
        yield (0x00, 0x40, 0x00)
        yield (0x00, 0x40, 0x40)
        yield (0x00, 0x00, 0x40)
        yield (0x40, 0x00, 0x40)


color = led_colors()
active = False
report = Report()
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
    report.buttons[A] = active * (t < 0.25)
    print(list(bytes(report)))
    try:
        gamepad.send_report(bytes(report))
    except OSError:
        print("Skipping due to OS error.")
