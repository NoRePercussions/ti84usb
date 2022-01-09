from ti84usb import packet, utils


class ErrorPacket(packet.VirtualPacket):
    type: 4
    subtype: 0xEE00

    error: bytes

    def __init__(self, error):
        self.error = error

    def _list(self):
        return [
            len(self)         .to_bytes(4, 'big'),
            self.type         .to_bytes(1, 'big'),
            len(self._raw_data()).to_bytes(4, 'big'),
            self.subtype      .to_bytes(2, 'big'),
            self.error
        ]

    def _raw_data(self):
        return self.error

    def __str__(self):
        out  = f"ERROR Packet {id(self)}" + "\n"
        out += f"  Error code: 0x{self.error.hex().upper()}" + "\n"
        out += f"  Human readable:" + "\n"
        out += f"    {self._human_readable_error()}"
        return out

    def _human_readable_error(self):
        error_lookup_table = {
            0x0004: "Invalid argument or name",
            0x0006: "Can't delete app",
            0x0008: "Transmission error / Invalid code",
            0x0009: "Cannot use basic mode packets while in boot mode",
            0x000C: "Out of memory",
            0x000D: "Invalid folder name",
            0x000E: "Invalid name",
            0x0011: "Busy",
            0x0012: "Variable is locked/archived",
            0x001C: "Mode token too small",
            0x001D: "Mode token too large",
            0x0022: "Invalid parameter ID/data",
            0x0029: "Unknwon remote control error",
            0x002B: "Battery low",
            0x0034: "Busy (not at home screen)",
        }

        int_error = int.from_bytes(self.error, 'big')
        if int_error in error_lookup_table:
            return error_lookup_table[int_error]
        else:
            return "Unknown error"

    @staticmethod
    def from_bytes(b):
        assert len(b) == 5 + 6 + 2, "Packet size is wrong"

        # 0  1  2  3   4   5  6  7  8   9  10   11 12
        # LL LL LL LL  TT  LL LL LL LL  TT TT  EE EE

        return ErrorPacket(
            error=b[11:]
        )