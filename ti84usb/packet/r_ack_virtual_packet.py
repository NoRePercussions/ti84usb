from ti84usb import packet
from warnings import warn


class AckVirtualPacket(packet.Packet):
    type: int = 5
    data: bytes

    def __init__(self, data=b'\xE0\x00'):
        self.data = data

    def _raw_data(self):
        return self.data

    def _list(self):
        return [
            len(self)   .to_bytes(4, 'big'),
            self.type   .to_bytes(1, 'big'),
            self._raw_data()
        ]

    @staticmethod
    def from_bytes(b):
        assert len(b) == 7, "Invalid acknowledgement packet: wrong size"
        if b[5:7] != b'\xE0\x00':
            warn(f"Invalid ACK code 0x{b[5:7].hex().upper()}")
        return AckVirtualPacket(b[5:7])
