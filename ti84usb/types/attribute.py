from ti84usb.types import *
from ti84usb import utils


# Attribute and Parameter are the same
class Attribute(Parameter):
    def __str__(self):
        out  = f"Parameter {hex(self.id)} {id(self)}" + "\n"
        if self.is_valid:
            out += f"  Value: {utils.format_bytes(self.data)}"
        else:
            out += f"  Invalid"

    def __str__(self):
        human_readable_attribs = {
            0x01: "Variable size",
            0x02: "Variable type",
            0x03: "Variable is archived",
            0x04: "Unknown",
            0x05: "AppVar source",
            0x08: "Variable is 83+ or 84+ only",
            0x11: "Variable type (request)",
            0x13: "Unknown (for deleting)",
            0x41: "Variable is locked",
            0x42: "Unknown",
        }

        if self.id in human_readable_attribs:
            start = f"Attribute {hex(self.id)} ({human_readable_attribs[self.id]}): "
        else:
            start = f"Attribute {hex(self.id)} (Unknown):" + "\n"

        if self.is_valid:
            end = f"{utils.format_bytes(self.data)}"
        else:
            end = f"Invalid"

        return start + end

    @staticmethod
    def from_bytes(b):
        attr_id = int.from_bytes(b[0:2], 'big')
        valid = (b[2] == 0)
        data_length = int.from_bytes(b[3:5], 'big')
        data = b[5:5+data_length]

        return Attribute(attr_id, valid, data)

    @staticmethod
    def from_bytes_assuming_valid(b):
        attr_id = int.from_bytes(b[0:2], 'big')
        valid = True
        data_length = int.from_bytes(b[2:4], 'big')
        data = b[4:4+data_length]

        return Attribute(attr_id, valid, data)