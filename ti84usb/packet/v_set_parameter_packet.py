from ti84usb import packet, utils
from ti84usb.types import Parameter


class SetParameterPacket(packet.VirtualPacket):
    type = 4
    subtype = 0x000E

    param: Parameter

    def __init__(self, param):
        self.param = param

    def _list(self):
        return [
            len(self)         .to_bytes(4, 'big'),
            self.type         .to_bytes(1, 'big'),
            len(self._raw_data()).to_bytes(4, 'big'),
            self.subtype      .to_bytes(2, 'big'),
            bytes(self.param)
        ]

    def _raw_data(self):
        return bytes(self.param)

    def __str__(self):
        out  = f"Set Parameter Packet {id(self)}" + "\n"
        out += f"  Parameter {self.param.id}: 0x{utils.format_bytes(self.param.data)}"
        return out

    @staticmethod
    def from_bytes(b):
        assert len(b) > 6, "Invalid packet: too small"  # Extra byte in header
        assert len(b) == 5 + int.from_bytes(b[0:4], 'big'), "Packet size mismatch"
        assert len(b) == 11 + int.from_bytes(b[5:9], 'big'), "Packet size mismatch"

        # 0  1  2  3   4   5  6  7  8   9 10   11 12  13 14  15 16
        # LL LL LL LL  TT  LL LL LL LL  TT TT  II II  LL LL  DD DD

        return SetParameterPacket(
            param=Parameter.from_bytes(b[11:])
        )
