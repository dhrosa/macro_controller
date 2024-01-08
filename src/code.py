import usb_hid
import time
import board
from neopixel_write import neopixel_write
import digitalio

gamepad = usb_hid.devices[0]

REPORT_LENGTH = 9

led_pin = digitalio.DigitalInOut(board.NEOPIXEL)
led_pin.switch_to_output()

def led_colors():
    while True:
        yield (0x40, 0x00, 0x00)
        yield (0x40, 0x40, 0x00)
        yield (0x00, 0x40, 0x00)
        yield (0x00, 0x40, 0x40)
        yield (0x00, 0x00, 0x40)
        yield (0x40, 0x00, 0x40)


color = led_colors()
while True:
    for byte_index in range(REPORT_LENGTH):
        for bit_index in range(8):
            report = bytearray(REPORT_LENGTH)
            report[byte_index] = (1 << bit_index)
            print(f"Sending report: {report.hex(' ')}")
            neopixel_write(led_pin, bytes(next(color)))
            try:
                gamepad.send_report(report)
            except OSError:
                print("Skipping due to OS error.")
