from ti84usb.packet import VirtualPacket


class AckSetModePacket(VirtualPacket):
    type = 4
    subtype = 0x0012
    constant: bytes = (2000).to_bytes(4, 'big')

    def __init__(self, constant=None):
        if constant:
            self.constant = constant

    def _raw_data(self):
        return self.constant

    @staticmethod
    def from_bytes(b):
        assert len(b) == 5 + 6 + 6, "Invalid packet: wrong size"


        # 0  1  2  3   4   5  6  7  8   9  10  11
        # LL LL LL LL  TT  LL LL LL LL  TT TT  DD DD DD DD DD DD
        return AckSetModePacket(
            constant=b[11:]
        )
