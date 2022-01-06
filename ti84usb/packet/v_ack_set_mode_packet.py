from ti84usb.packet import VirtualPacket


class AckSetModePacket(VirtualPacket):
    type = 4
    subtype = 0x12
    is_final = True
    constant: bytes = (2000).to_bytes(4, 'big')

    def __init__(self, constant=None):
        if constant:
            self.constant = constant

    def _raw_data(self):
        return self.constant

    @staticmethod
    def from_bytes(b):
        assert len(b) == 6 + 4, "Invalid packet: wrong size"

        return AckSetModePacket(
            constant=b[6:]
        )
