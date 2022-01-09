from ti84usb.types import *


# Attribute and Parameter are the same
class Attribute(Parameter):
    def __str__(self):
        out  = f"Parameter {hex(self.id)} {id(self)}" + "\n"
        if self.is_valid:
            out += f"  Value: {utils.format_bytes(self.data)}"
        else:
            out += f"  Invalid"

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