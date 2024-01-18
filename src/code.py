from board import board_id
from sys import exit

print(f"\n{board_id=}")

if board_id == 'adafruit_macropad_rp2040':
    import adafruit_macropad_rp2040
    exit()
