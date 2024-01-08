import usb_hid
import supervisor

DESCRIPTOR = "05010905a10115002501350045017501950e05091901290e81029502810105012507463b017504950165140939814265009501810126ff0046ff000930093109320935750895048102750895018101c0"

supervisor.set_usb_identification(vid=0x0F0D,pid=0x00C1)

gamepad = usb_hid.Device(
    report_descriptor=bytes.fromhex(DESCRIPTOR),
    usage_page = 0x01, # Generic Desktop Control
    usage = 0x05, # Gamepad
    report_ids=(0,), # No report ID used
    in_report_lengths=(9,),
    out_report_lengths=(0,), # We don't receive any reports.
 )

usb_hid.enable((gamepad,))
