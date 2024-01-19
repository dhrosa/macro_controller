from board import board_id

print(f"\n{board_id=}")

if board_id == "adafruit_macropad_rp2040":
    import code_macropad  # noqa
elif board_id == "adafruit_feather_rp2040":
    import code_feather  # noqa
