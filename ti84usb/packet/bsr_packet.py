from ti84usb import packet


class BufferSizeRequestPacket(packet.Packet):
    type: int = 1
    buffer_size: int

    def __init__(self, buffer_size=0x400):
        self.buffer_size = buffer_size

    def _raw_data(self):
        return self.buffer_size.to_bytes(4, 'big')

    @staticmethod
    def from_bytes(b):
        assert len(b) == 9, "Invalid packet: wrong size"
        return BufferSizeRequestPacket(
            buffer_size=int.from_bytes(b[5:], 'big')
        )
