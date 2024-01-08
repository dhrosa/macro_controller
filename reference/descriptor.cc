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
  HID_RI_USAGE_PAGE(8,1),                         // Generic desktop controls
    HID_RI_USAGE(8,5),                              // Joystick
    HID_RI_COLLECTION(8,1),                         // Application

    // Buttons (2 bytes)
    HID_RI_LOGICAL_MINIMUM(8,0),                    // button off state
    HID_RI_LOGICAL_MAXIMUM(8,1),                    // button on state
    HID_RI_PHYSICAL_MINIMUM(8,0),                   // button off state
    HID_RI_PHYSICAL_MAXIMUM(8,1),                   // button on state
    HID_RI_REPORT_SIZE(8,1),                        // 1 bit per report field
    HID_RI_REPORT_COUNT(8,14),                      // 14 report fields (14 buttons)
    HID_RI_USAGE_PAGE(8,9),                         // Buttons (section 12)
    HID_RI_USAGE_MINIMUM(8,1),
    HID_RI_USAGE_MAXIMUM(8,14),
    HID_RI_INPUT(8,2),                              // Variable input
    HID_RI_REPORT_COUNT(8,2),                       // 2 report fields (empty 2 bits)
    HID_RI_INPUT(8,1),                              // Array input

    // HAT switch
    HID_RI_USAGE_PAGE(8,1),                         // Generic desktop controls
    HID_RI_LOGICAL_MAXIMUM(8,7),                    // 8 valid HAT states, sending 0x08 = nothing pressed
    HID_RI_PHYSICAL_MAXIMUM(16,315),                // HAT "rotation"
    HID_RI_REPORT_SIZE(8,4),                        // 4 bits per report field
    HID_RI_REPORT_COUNT(8,1),                       // 1 report field (a nibble containing entire HAT state)
    HID_RI_UNIT(8,20),                              // unit degrees
    HID_RI_USAGE(8,57),                             // Hat switch (section 4.3)
    HID_RI_INPUT(8,66),                             // Variable input, null state
    HID_RI_UNIT(8,0),                               // No units
    HID_RI_REPORT_COUNT(8,1),                       // 1 report field (empty upper nibble)
    HID_RI_INPUT(8,1),                              // Array input

    // Joystick (4 bytes)
    HID_RI_LOGICAL_MAXIMUM(16,255),                 // 0-255 for analog sticks
    HID_RI_PHYSICAL_MAXIMUM(16,255),
    HID_RI_USAGE(8,48),                             // X (left X)
    HID_RI_USAGE(8,49),                             // Y (left Y)
    HID_RI_USAGE(8,50),                             // Z (right X)
    HID_RI_USAGE(8,53),                             // Rz (right Y)
    HID_RI_REPORT_SIZE(8,8),                        // 1 byte per report field
    HID_RI_REPORT_COUNT(8,4),                       // 4 report fields (left X, left Y, right X, right Y)
    HID_RI_INPUT(8,2),                              // Variable input

    // I think this is the vendor spec byte.
    // On the Pokken pad this is usage page 0xFF00 which is vendor defined.
    // Usage is 0x20 on the Pokken pad, but since the usage page is vendor defined this is kind of meaningless.
    // Seems fine to just leave this byte set to 0.
    HID_RI_REPORT_SIZE(8,8),                        // 1 byte per report field
    HID_RI_REPORT_COUNT(8,1),                       // 1 report field
    HID_RI_INPUT(8,1),                              // Array input
    HID_RI_END_COLLECTION(0),
    };
