import usb_hid

HID_DESCRIPTOR = [
    0x05,
    0x01,  # Usage Page (Generic Desktop Ctrls)
    0x09,
    0x05,  # Usage (Game Pad)
    0xA1,
    0x01,  # Collection (Application)
    0x15,
    0x00,  #   Logical Minimum (0)
    0x25,
    0x01,  #   Logical Maximum (1)
    0x35,
    0x00,  #   Physical Minimum (0)
    0x45,
    0x01,  #   Physical Maximum (1)
    0x75,
    0x01,  #   Report Size (1)
    0x95,
    0x10,  #   Report Count (16)
    0x05,
    0x09,  #   Usage Page (Button)
    0x19,
    0x01,  #   Usage Minimum (0x01)
    0x29,
    0x10,  #   Usage Maximum (0x10)
    0x81,
    0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x05,
    0x01,  #   Usage Page (Generic Desktop Ctrls)
    0x25,
    0x07,  #   Logical Maximum (7)
    0x46,
    0x3B,
    0x01,  #   Physical Maximum (315)
    0x75,
    0x04,  #   Report Size (4)
    0x95,
    0x01,  #   Report Count (1)
    0x65,
    0x14,  #   Unit (System: English Rotation, Length: Centimeter)
    0x09,
    0x39,  #   Usage (Hat switch)
    0x81,
    0x42,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,Null State)
    0x65,
    0x00,  #   Unit (None)
    0x95,
    0x01,  #   Report Count (1)
    0x81,
    0x01,  #   Input (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x26,
    0xFF,
    0x00,  #   Logical Maximum (255)
    0x46,
    0xFF,
    0x00,  #   Physical Maximum (255)
    0x09,
    0x30,  #   Usage (X)
    0x09,
    0x31,  #   Usage (Y)
    0x09,
    0x32,  #   Usage (Z)
    0x09,
    0x35,  #   Usage (Rz)
    0x75,
    0x08,  #   Report Size (8)
    0x95,
    0x04,  #   Report Count (4)
    0x81,
    0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x06,
    0x00,
    0xFF,  #   Usage Page (Vendor Defined 0xFF00)
    0x09,
    0x20,  #   Usage (0x20)
    0x95,
    0x01,  #   Report Count (1)
    0x81,
    0x02,  #   Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x0A,
    0x21,
    0x26,  #   Usage (0x2621)
    0x95,
    0x08,  #   Report Count (8)
    0x91,
    0x02,  #   Output (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position,Non-volatile)
    0xC0,  # End Collection
]

gamepad = usb_hid.Device(
    report_descriptor=bytes(HID_DESCRIPTOR),
    usage_page = 0x01, # Generic Desktop Control
    usage = 0x05, # Gamepad
    report_ids=(0,), # No report ID used
    in_report_lengths=(9,),
    out_report_lengths=(0,), # We don't receive any reports.
 )

usb_hid.enable((gamepad,))
