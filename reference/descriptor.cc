// Derived from https://github.com/KawaSwitch/Poke-Controller/blob/master/Descriptors.c

#define CONCAT(x, y) x##y
#define CONCAT_EXPANDED(x, y) CONCAT(x, y)

#define HID_RI_DATA_SIZE_MASK 0x03
#define HID_RI_TYPE_MASK 0x0C
#define HID_RI_TAG_MASK 0xF0

#define HID_RI_TYPE_MAIN 0x00
#define HID_RI_TYPE_GLOBAL 0x04
#define HID_RI_TYPE_LOCAL 0x08

#define HID_RI_DATA_BITS_0 0x00
#define HID_RI_DATA_BITS_8 0x01
#define HID_RI_DATA_BITS_16 0x02
#define HID_RI_DATA_BITS_32 0x03
#define HID_RI_DATA_BITS(DataBits) CONCAT_EXPANDED(HID_RI_DATA_BITS_, DataBits)

#define _HID_RI_ENCODE_0(Data)
#define _HID_RI_ENCODE_8(Data) , (Data & 0xFF)
#define _HID_RI_ENCODE_16(Data)                                                \
  _HID_RI_ENCODE_8(Data) _HID_RI_ENCODE_8(Data >> 8)
#define _HID_RI_ENCODE_32(Data)                                                \
  _HID_RI_ENCODE_16(Data) _HID_RI_ENCODE_16(Data >> 16)
#define _HID_RI_ENCODE(DataBits, ...)                                          \
  CONCAT_EXPANDED(_HID_RI_ENCODE_, DataBits(__VA_ARGS__))

#define _HID_RI_ENTRY(Type, Tag, DataBits, ...)                                \
  (Type | Tag | HID_RI_DATA_BITS(DataBits))                                    \
      _HID_RI_ENCODE(DataBits, (__VA_ARGS__))

#define HID_IOF_CONSTANT                        (1 << 0)
#define HID_IOF_DATA                            (0 << 0)
#define HID_IOF_VARIABLE                        (1 << 1)
#define HID_IOF_ARRAY                           (0 << 1)
#define HID_IOF_RELATIVE                        (1 << 2)
#define HID_IOF_ABSOLUTE                        (0 << 2)
#define HID_IOF_WRAP                            (1 << 3)
#define HID_IOF_NO_WRAP                         (0 << 3)
#define HID_IOF_NON_LINEAR                      (1 << 4)
#define HID_IOF_LINEAR                          (0 << 4)
#define HID_IOF_NO_PREFERRED_STATE              (1 << 5)
#define HID_IOF_PREFERRED_STATE                 (0 << 5)
#define HID_IOF_NULLSTATE                       (1 << 6)
#define HID_IOF_NO_NULL_POSITION                (0 << 6)
#define HID_IOF_VOLATILE                        (1 << 7)
#define HID_IOF_NON_VOLATILE                    (0 << 7)
#define HID_IOF_BUFFERED_BYTES                  (1 << 8)
#define HID_IOF_BITFIELD                        (0 << 8)

#define HID_RI_INPUT(DataBits, ...)             _HID_RI_ENTRY(HID_RI_TYPE_MAIN  , 0x80, DataBits, __VA_ARGS__)
#define HID_RI_OUTPUT(DataBits, ...)            _HID_RI_ENTRY(HID_RI_TYPE_MAIN  , 0x90, DataBits, __VA_ARGS__)
#define HID_RI_COLLECTION(DataBits, ...)        _HID_RI_ENTRY(HID_RI_TYPE_MAIN  , 0xA0, DataBits, __VA_ARGS__)
#define HID_RI_FEATURE(DataBits, ...)           _HID_RI_ENTRY(HID_RI_TYPE_MAIN  , 0xB0, DataBits, __VA_ARGS__)
#define HID_RI_END_COLLECTION(DataBits, ...)    _HID_RI_ENTRY(HID_RI_TYPE_MAIN  , 0xC0, DataBits, __VA_ARGS__)
#define HID_RI_USAGE_PAGE(DataBits, ...)        _HID_RI_ENTRY(HID_RI_TYPE_GLOBAL, 0x00, DataBits, __VA_ARGS__)
#define HID_RI_LOGICAL_MINIMUM(DataBits, ...)   _HID_RI_ENTRY(HID_RI_TYPE_GLOBAL, 0x10, DataBits, __VA_ARGS__)
#define HID_RI_LOGICAL_MAXIMUM(DataBits, ...)   _HID_RI_ENTRY(HID_RI_TYPE_GLOBAL, 0x20, DataBits, __VA_ARGS__)
#define HID_RI_PHYSICAL_MINIMUM(DataBits, ...)  _HID_RI_ENTRY(HID_RI_TYPE_GLOBAL, 0x30, DataBits, __VA_ARGS__)
#define HID_RI_PHYSICAL_MAXIMUM(DataBits, ...)  _HID_RI_ENTRY(HID_RI_TYPE_GLOBAL, 0x40, DataBits, __VA_ARGS__)
#define HID_RI_UNIT_EXPONENT(DataBits, ...)     _HID_RI_ENTRY(HID_RI_TYPE_GLOBAL, 0x50, DataBits, __VA_ARGS__)
#define HID_RI_UNIT(DataBits, ...)              _HID_RI_ENTRY(HID_RI_TYPE_GLOBAL, 0x60, DataBits, __VA_ARGS__)
#define HID_RI_REPORT_SIZE(DataBits, ...)       _HID_RI_ENTRY(HID_RI_TYPE_GLOBAL, 0x70, DataBits, __VA_ARGS__)
#define HID_RI_REPORT_ID(DataBits, ...)         _HID_RI_ENTRY(HID_RI_TYPE_GLOBAL, 0x80, DataBits, __VA_ARGS__)
#define HID_RI_REPORT_COUNT(DataBits, ...)      _HID_RI_ENTRY(HID_RI_TYPE_GLOBAL, 0x90, DataBits, __VA_ARGS__)
#define HID_RI_PUSH(DataBits, ...)              _HID_RI_ENTRY(HID_RI_TYPE_GLOBAL, 0xA0, DataBits, __VA_ARGS__)
#define HID_RI_POP(DataBits, ...)               _HID_RI_ENTRY(HID_RI_TYPE_GLOBAL, 0xB0, DataBits, __VA_ARGS__)
#define HID_RI_USAGE(DataBits, ...)             _HID_RI_ENTRY(HID_RI_TYPE_LOCAL , 0x00, DataBits, __VA_ARGS__)
#define HID_RI_USAGE_MINIMUM(DataBits, ...)     _HID_RI_ENTRY(HID_RI_TYPE_LOCAL , 0x10, DataBits, __VA_ARGS__)
#define HID_RI_USAGE_MAXIMUM(DataBits, ...)     _HID_RI_ENTRY(HID_RI_TYPE_LOCAL , 0x20, DataBits, __VA_ARGS__)

const unsigned char descriptor[] = {
    HID_RI_USAGE_PAGE(8, 1), /* Generic Desktop */
    HID_RI_USAGE(8, 5),      /* Joystick */
    HID_RI_COLLECTION(8, 1), /* Application */
    // Buttons (2 bytes)
    HID_RI_LOGICAL_MINIMUM(8, 0),
    HID_RI_LOGICAL_MAXIMUM(8, 1),
    HID_RI_PHYSICAL_MINIMUM(8, 0),
    HID_RI_PHYSICAL_MAXIMUM(8, 1),
    // The Switch will allow us to expand the original HORI descriptors to a
    // full 16 buttons. The Switch will make use of 14 of those buttons.
    HID_RI_REPORT_SIZE(8, 1),
    HID_RI_REPORT_COUNT(8, 16),
    HID_RI_USAGE_PAGE(8, 9),
    HID_RI_USAGE_MINIMUM(8, 1),
    HID_RI_USAGE_MAXIMUM(8, 16),
    HID_RI_INPUT(8, 2),
    // HAT Switch (1 nibble)
    HID_RI_USAGE_PAGE(8, 1),
    HID_RI_LOGICAL_MAXIMUM(8, 7),
    HID_RI_PHYSICAL_MAXIMUM(16, 315),
    HID_RI_REPORT_SIZE(8, 4),
    HID_RI_REPORT_COUNT(8, 1),
    HID_RI_UNIT(8, 20),
    HID_RI_USAGE(8, 57),
    HID_RI_INPUT(8, 66),
    // There's an additional nibble here that's utilized as part of the Switch
    // Pro Controller. I believe this -might- be separate U/D/L/R bits on the
    // Switch Pro Controller, as they're utilized as four button descriptors on
    // the Switch Pro Controller.
    HID_RI_UNIT(8, 0),
    HID_RI_REPORT_COUNT(8, 1),
    HID_RI_INPUT(8, 1),
    // Joystick (4 bytes)
    HID_RI_LOGICAL_MAXIMUM(16, 255),
    HID_RI_PHYSICAL_MAXIMUM(16, 255),
    HID_RI_USAGE(8, 48),
    HID_RI_USAGE(8, 49),
    HID_RI_USAGE(8, 50),
    HID_RI_USAGE(8, 53),
    HID_RI_REPORT_SIZE(8, 8),
    HID_RI_REPORT_COUNT(8, 4),
    HID_RI_INPUT(8, 2),
    // ??? Vendor Specific (1 byte)
    // This byte requires additional investigation.
    HID_RI_USAGE_PAGE(16, 65280),
    HID_RI_USAGE(8, 32),
    HID_RI_REPORT_COUNT(8, 1),
    HID_RI_INPUT(8, 2),
    // Output (8 bytes)
    // Original observation of this suggests it to be a mirror of the inputs
    // that we sent. The Switch requires us to have these descriptors available.
    HID_RI_USAGE(16, 9761),
    HID_RI_REPORT_COUNT(8, 8),
    HID_RI_OUTPUT(8, 2),
    HID_RI_END_COLLECTION(0),
};
