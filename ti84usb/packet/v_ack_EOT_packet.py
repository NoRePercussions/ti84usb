from ti84usb import packet, utils


class AckEOTPacket(packet.VirtualPacket):
    type = 4
    subtype = 0x0006
    success: bool

    def __init__(self, success=True):
        self.success = success

    def _raw_data(self):
        return b'\x01' if self.success else b'\x00'

    def __str__(self):
        out   = f"ACK EOT Packet {id(self)}" + "\n"
        out  += f"  Success: {self.success}"
        return out

    @staticmethod
    def from_bytes(b):
        assert len(b) == 5 + 6 + 1, "Invalid packet: wrong size"

        # 0  1  2  3   4   5  6  7  8   9  10  11
        # LL LL LL LL  TT  LL LL LL LL  TT TT  DD
        return AckEOTPacket(
            success=(b[11] == b'\x01')
        )
