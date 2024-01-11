import supervisor
import usb_hid

DESCRIPTOR = [
    0x05,
    0x01,  # Usage Page (Generic Desktop Ctrls)
    0x09,
    0x05,  # Usage (Game Pad)
    0xA1,
    0x01,  # Collection (Application)
    0x15,
    0x00,  # Logical Minimum (0)
    0x25,
    0x01,  # Logical Maximum (1)
    0x35,
    0x00,  # Physical Minimum (0)
    0x45,
    0x01,  # Physical Maximum (1)
    0x75,
    0x01,  # Report Size (1)
    0x95,
    0x0E,  # Report Count (14)
    0x05,
    0x09,  # Usage Page (Button)
    0x19,
    0x01,  # Usage Minimum (0x01)
    0x29,
    0x0E,  # Usage Maximum (0x0E)
    0x81,
    0x02,  # Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x95,
    0x02,  # Report Count (2)
    0x81,
    0x01,  # Input (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x05,
    0x01,  # Usage Page (Generic Desktop Ctrls)
    0x25,
    0x07,  # Logical Maximum (7)
    0x46,
    0x3B,
    0x01,  # Physical Maximum (315)
    0x75,
    0x04,  # Report Size (4)
    0x95,
    0x01,  # Report Count (1)
    0x65,
    0x14,  # Unit (System: English Rotation, Length: Centimeter)
    0x09,
    0x39,  # Usage (Hat switch)
    0x81,
    0x42,  # Input (Data,Var,Abs,No Wrap,Linear,Preferred State,Null State)
    0x65,
    0x00,  # Unit (None)
    0x95,
    0x01,  # Report Count (1)
    0x81,
    0x01,  # Input (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x26,
    0xFF,
    0x00,  # Logical Maximum (255)
    0x46,
    0xFF,
    0x00,  # Physical Maximum (255)
    0x09,
    0x30,  # Usage (X)
    0x09,
    0x31,  # Usage (Y)
    0x09,
    0x32,  # Usage (Z)
    0x09,
    0x35,  # Usage (Rz)
    0x75,
    0x08,  # Report Size (8)
    0x95,
    0x04,  # Report Count (4)
    0x81,
    0x02,  # Input (Data,Var,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0x75,
    0x08,  # Report Size (8)
    0x95,
    0x01,  # Report Count (1)
    0x81,
    0x01,  # Input (Const,Array,Abs,No Wrap,Linear,Preferred State,No Null Position)
    0xC0,  # End Collection
]

# USB vendor and product ID for "Hori Co., Ltd HORIPAD for Nintendo Switch".
#
# TODO(dhrosa): Check if the Switch actually cares about the VID/PID, or if a
# correct HID descriptor is sufficient.
supervisor.set_usb_identification(vid=0x0F0D, pid=0x00C1)

gamepad = usb_hid.Device(
    report_descriptor=bytes(DESCRIPTOR),
    usage_page=0x01,  # Generic Desktop Control
    usage=0x05,  # Gamepad
    report_ids=(0,),  # No report ID used
    in_report_lengths=(9,),
    out_report_lengths=(0,),  # We don't receive any reports.
)

usb_hid.enable((gamepad,))
