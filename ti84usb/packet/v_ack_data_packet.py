from ti84usb import packet, utils


class AckDataPacket(packet.VirtualPacket):
    type = 4
    subtype = 0xAA00
    constant = b'\x01'

    def __init__(self):
        # Don't want to send to super __init__!
        pass

    def _raw_data(self):
        return self.constant

    def __str__(self):
        out  = f"ACK Data Packet {id(self)}" + "\n"
        return out

    @staticmethod
    def from_bytes(b):
        assert len(b) == 5 + 6 + 1, "Invalid packet: wrong size"

        # 0  1  2  3   4   5  6  7  8   9  10  11
        # LL LL LL LL  TT  LL LL LL LL  TT TT  DD
        return AckDataPacket()
