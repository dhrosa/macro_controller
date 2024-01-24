from bitfield import Bitfield
from enums import hat


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
