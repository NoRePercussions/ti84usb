from ti84usb.packet import VirtualPacket


class SetModePacket(VirtualPacket):
    type = 4
    subtype = 0x0001
    is_final = True

    constant: int = (2000).to_bytes(4, 'big')
    mode_template = b'\x00\x0F\x00\x01\x00\x00'

    mode: int

    def __init__(self, mode, constant=None):
        if type(mode) is int:
            self.mode = mode
        else:
            self.mode = mode[1]
        if constant:
            self.constant = constant

    def _raw_data(self):
        temp = bytearray(self.mode_template)
        temp[1] = self.mode
        return bytes(temp) + self.constant

    @staticmethod
    def from_bytes(b):
        assert len(b) == 5 + 6 + 10, "Invalid packet: wrong size"

        return SetModePacket(
            mode=b[11:17],
            constant=b[17:]
        )
