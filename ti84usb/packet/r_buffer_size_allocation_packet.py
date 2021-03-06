from ti84usb import packet, utils


class BufferSizeAllocationPacket(packet.Packet):
    type: int = 2
    buffer_size: int

    def __init__(self, buffer_size=0x400):
        self.buffer_size = buffer_size

    def _raw_data(self):
        return self.buffer_size.to_bytes(4, 'big')

    def __str__(self):
        out  = f"Buffer Size Allocation Packet {id(self)}" + "\n"
        out += f"  Buffer size: {self.buffer_size} bytes"
        return out

    @staticmethod
    def from_bytes(b):
        assert len(b) == 9, "Invalid packet: wrong size"
        return BufferSizeAllocationPacket(
            buffer_size=int.from_bytes(b[5:], 'big')
        )
