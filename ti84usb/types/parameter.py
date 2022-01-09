from ti84usb import utils


class Parameter:
    id: int
    is_valid: bool
    data: bytes = None

    def __init__(self, id, is_valid=True, data=None):
        self.id = id
        self.is_valid = is_valid
        if is_valid and isinstance(data, bytes):
            self.data = data
        elif is_valid and isinstance(data, int) and is_valid < 16:
            self.data = data.to_bytes(1, 'big')

    def __bytes__(self):
        out = self.id.to_bytes(2, 'big')
        out += b'\x00' if self.is_valid else b'\x01'
        if self.is_valid:
            out += len(self.data).to_bytes(2, 'big')
            out += self.data
        return out

    def bytes_assuming_valid(self):
        out = self.id.to_bytes(2, 'big')
        if self.is_valid:
            out += len(self.data).to_bytes(2, 'big')
            out += self.data
        return out

    def __repr__(self):
        return f"{type(self).__name__}{hex(self.id)}<{id(self)}>"

    def __str__(self):
        out  = f"Parameter {hex(self.id)} {id(self)}" + "\n"
        if self.is_valid:
            out += f"  Value: {utils.format_bytes(self.data)}"
        else:
            out += f"  Invalid"

    @staticmethod
    def from_bytes(b):
        param_id = int.from_bytes(b[0:2], 'big')
        valid = (b[2] == 0)
        data_length = int.from_bytes(b[3:5], 'big')
        data = b[5:5+data_length]

        return Parameter(param_id, valid, data)

    @staticmethod
    def from_bytes_assuming_valid(b):
        param_id = int.from_bytes(b[0:2], 'big')
        valid = True
        data_length = int.from_bytes(b[2:4], 'big')
        data = b[4:4+data_length]

        return Parameter(param_id, valid, data)
