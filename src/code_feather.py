import asyncio

import board
import digitalio
import neopixel
import usb_hid
from adafruit_debouncer import Button

from enums import buttons
from report import Report

# Using NeoKey FeatherWing: https://www.adafruit.com/product/4979

gamepad = usb_hid.devices[0]
report = Report()

pixels = neopixel.NeoPixel(board.D9, 2)
switches = []
for p in (board.D5, board.D6):
    pin = digitalio.DigitalInOut(p)
    pin.pull = digitalio.Pull.UP
    switches.append(Button(pin))

pixels.brightness = 0.1

pulse_active = asyncio.Event()
target_button = None

speed_exponent = 1


async def update_switches() -> None:
    global speed_exponent
    global target_button
    while True:
        for i, sw in enumerate(switches):
            sw.update()

        button_switch, speed_switch = switches

        if speed_switch.short_count == 2:
            speed_exponent -= 1
            print(pow(1.1, speed_exponent))
        elif speed_switch.long_press:
            speed_exponent += 1
            print(pow(1.1, speed_exponent))

        if button_switch.short_count | button_switch.long_press:
            if target_button is None:
                target_button = buttons.A
                pulse_active.set()
            elif target_button == buttons.A:
                target_button = buttons.Y
                pulse_active.set()
            else:
                target_button = None
                pulse_active.clear()

        await asyncio.sleep(0.001)


async def pulse() -> None:
    while True:
        await pulse_active.wait()
        button = target_button
        if button is None:
            continue

        color = (0, 0, 0xFF) if button == buttons.A else (0xFF, 0xFF, 0)

        pixels.fill(color)
        report.buttons[button] = True
        await asyncio.sleep(0.1)

        report.buttons[button] = False
        pixels.fill((0, 0, 0))
        low_time = pow(1.1, speed_exponent)
        await asyncio.sleep(low_time)


async def send_hid_reports() -> None:
    last_payload = None
    while True:
        payload = bytes(report)
        if payload != last_payload:
            last_payload = payload
            print(f"Payload: {payload.hex()}")
        try:
            gamepad.send_report(payload)
        except OSError as e:
            print(f"HID report unsent: {e}")
        await asyncio.sleep(0.01)


asyncio.run(
    asyncio.gather(
        update_switches(),
        pulse(),
        send_hid_reports(),
    )  # type: ignore[arg-type]
)
