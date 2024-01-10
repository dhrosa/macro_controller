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


class Buttons:
    def __init__(self):
        self.data = 0

    def __getitem__(self, index):
        mask = 1 << index
        return bool(self.data & mask)

    def __setitem__(self, index, value):
        mask = 1 << index
        if value:
            self.data |= mask
        else:
            self.data &= ~mask

    def __str__(self):
        return f"{self.data:2X}"

    def __bytes__(self):
        return self.data.to_bytes(2, "little")
