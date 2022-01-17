from ti84usb import packet, utils


class EOTPacket(packet.VirtualPacket):
    type = 4
    subtype = 0xDD00

    def __init__(self, success=True):
        pass

    def _raw_data(self):
        return b''

    def __str__(self):
        out = f"EOT Packet {id(self)}"
        return out

    @staticmethod
    def from_bytes(b):
        assert len(b) == 5 + 6, "Invalid packet: wrong size"

        # 0  1  2  3   4   5  6  7  8   9  10
        # LL LL LL LL  TT  LL LL LL LL  TT TT
        return EOTPacket()
