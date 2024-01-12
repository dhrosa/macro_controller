import asyncio
from asyncio.event import Event

import keypad
from adafruit_simple_text_display import SimpleTextDisplay

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


class buttons:
    Y = 0
    B = 1
    A = 2
    X = 3
    L = 4
    R = 5
    ZL = 6
    ZR = 7
    MINUS = 8
    PLUS = 9
    LS = 10
    RS = 11


class hat:
    N = 0
    NE = 1
    E = 2
    SE = 3
    S = 4
    SW = 5
    W = 6
    NW = 7
    CENTER = 8


class keys:
    L = 0
    UP = 1
    R = 2
    LEFT = 3
    PULSE = 4
    RIGHT = 5
    Y = 6
    DOWN = 7
    X = 8
    B = 9
    PLUS = 10
    A = 11


def map_analog_value(value: float) -> int:
    """Maps analog values [-1.0, 1.0] to integer range [0, 255]."""
    if value < -1.0 or value > 1.0:
        raise ValueError(value)
    return int(128 + value * 127.5)


class Report:
    """High-level HID report payload wrapper"""

    def __init__(self) -> None:
        # 16-bit (2 bytes) button bitfield
        self.buttons = Bitfield(16)
        # 4-bit (1 byte) HAT switch state
        self.hat = hat.CENTER
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

pulse_active = Event()
report = Report()


async def pulse() -> None:
    color = led_colors()
    while True:
        await pulse_active.wait()

        macropad.pixels[keys.PULSE] = next(color)
        report.buttons[buttons.A] = True
        await asyncio.sleep(0.25)

        report.buttons[buttons.A] = False
        macropad.pixels[keys.PULSE] = (0, 0, 0)
        await asyncio.sleep(0.75)


def handle_directional_key(event: keypad.Event) -> None:
    k = event.key_number
    pressed = event.pressed
    released = event.released
    if (k == keys.UP and pressed) or (k == keys.DOWN and released):
        report.ly -= 1
    if (k == keys.UP and released) or (k == keys.DOWN and pressed):
        report.ly += 1

    if (k == keys.LEFT and pressed) or (k == keys.RIGHT and released):
        report.lx -= 1
    if (k == keys.LEFT and released) or (k == keys.RIGHT and pressed):
        report.lx += 1


def handle_simple_key(event: keypad.Event) -> None:
    direct_buttons = {
        keys.L: buttons.L,
        keys.R: buttons.R,
        keys.Y: buttons.Y,
        keys.X: buttons.X,
        keys.B: buttons.B,
        keys.PLUS: buttons.PLUS,
        keys.A: buttons.A,
    }
    button = direct_buttons.get(event.key_number)
    if button is None:
        return
    report.buttons[button] = event.pressed


async def handle_keys() -> None:
    while True:
        event = macropad.keys.events.get()
        if not event:
            await asyncio.sleep(0.1)
            continue

        handle_simple_key(event)
        handle_directional_key(event)
        if event.key_number == keys.PULSE and event.pressed:
            if pulse_active.is_set():
                pulse_active.clear()
            else:
                pulse_active.set()


def render_report(lines: SimpleTextDisplay) -> None:
    lines[0].text = " ".join(
        (
            "B" if report.buttons[buttons.B] else " ",
            "A" if report.buttons[buttons.A] else " ",
            "X" if report.buttons[buttons.X] else " ",
            "Y" if report.buttons[buttons.Y] else " ",
            "L" if report.buttons[buttons.L] else " ",
            "R" if report.buttons[buttons.R] else " ",
            "-" if report.buttons[buttons.MINUS] else " ",
        )
    )

    lines[1].text = " ".join(
        (
            "LEFT" if report.lx < 0 else " " * 4,
            "RIGHT" if report.lx > 0 else " " * 5,
            "UP" if report.ly < 0 else " " * 2,
            "DOWN" if report.ly > 0 else " " * 4,
        )
    )
    lines.show()


async def send_hid_reports() -> None:
    lines = macropad.display_text(title="Last Report:")
    last_payload = None
    while True:
        payload = bytes(report)
        if payload != last_payload:
            last_payload = payload
            render_report(lines)
        try:
            gamepad.send_report(payload)
        except OSError as e:
            print(f"HID report unsent: {e}")
        await asyncio.sleep(0.01)


asyncio.run(asyncio.gather(pulse(), handle_keys(), send_hid_reports()))  # type: ignore[arg-type]
