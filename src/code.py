import asyncio
from asyncio.event import Event

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
    if value < -1.0 or value > 1.0:
        raise ValueError(value)
    return int(128 + value * 127)


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
        # Unused vendor-specific byte.
        vendor_specific = 0
        return bytes(self.buttons) + bytes(
            (
                self.hat,
                map_analog_value(self.lx),
                map_analog_value(self.ly),
                map_analog_value(self.rx),
                map_analog_value(self.ry),
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


async def main() -> None:
    pass


asyncio.run(main())

active = Event()
report = Report()


async def pulse() -> None:
    color = led_colors()
    while True:
        await active.wait()

        macropad.pixels.fill(next(color))
        report.buttons[A] = True
        await asyncio.sleep(0.25)

        report.buttons[A] = False
        macropad.pixels.fill((0, 0, 0))
        await asyncio.sleep(0.75)


async def handle_keys() -> None:
    while True:
        while event := macropad.keys.events.get():
            if event.pressed:
                print("Key press")
                if active.is_set():
                    active.clear()
                else:
                    active.set()
            else:
                print("Key release")
        await asyncio.sleep(0.1)


async def send_hid_reports() -> None:
    while True:
        try:
            gamepad.send_report(bytes(report))
        except OSError as e:
            print(f"HID report unsent: {e}")
        await asyncio.sleep(0.01)


asyncio.run(asyncio.gather(pulse(), handle_keys(), send_hid_reports()))  # type: ignore[arg-type]
