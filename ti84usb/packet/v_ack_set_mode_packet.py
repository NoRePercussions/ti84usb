from ti84usb import packet, utils


class AckSetModePacket(packet.VirtualPacket):
    type = 4
    subtype = 0x0012
    suffix: bytes = (2000).to_bytes(4, 'big')

    def __init__(self, suffix=None):
        if suffix:
            self.suffix = suffix

    def _raw_data(self):
        return self.suffix

    def __str__(self):
        out   = f"ACK Set Mode Packet {id(self)}" + "\n"
        out  += f"  Suffix: {utils.format_bytes(self.suffix)}"
        return out

    @staticmethod
    def from_bytes(b):
        assert len(b) == 5 + 6 + 4, "Invalid packet: wrong size"


        # 0  1  2  3   4   5  6  7  8   9  10  11
        # LL LL LL LL  TT  LL LL LL LL  TT TT  DD DD DD DD
        return AckSetModePacket(
            suffix=b[11:]
        )
