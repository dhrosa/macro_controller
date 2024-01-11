try:
    from typing import Any
except ImportError:
    pass


class Bitfield:
    """Bit-wise indexing into an integer."""

    def __init__(self, width: int):
        self.width = width
        self.data = 0

    def __getitem__(self, index: int) -> bool:
        mask = 1 << index
        return bool(self.data & mask)

    def __setitem__(self, index: int, value: Any) -> None:
        mask = 1 << index
        if value:
            self.data |= mask
        else:
            self.data &= ~mask

    def __str__(self) -> str:
        return f"{self.data:2X}"

    def __bytes__(self) -> bytes:
        return self.data.to_bytes(self.width // 8, "little")
