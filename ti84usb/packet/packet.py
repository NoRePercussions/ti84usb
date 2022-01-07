import ti84usb as ti
import ti84usb.util as util
import ti84usb.packet as packet
from warnings import warn

class Packet:
    type: int
    data: bytes

    def __init__(self, type=None, data=None):
        self.type = type
        self.data = data

    def __len__(self):
        return len(self._raw_data())

    def _list(self):
        return [
            len(self)   .to_bytes(4, 'big'),
            self.type   .to_bytes(1, 'big'),
            self._raw_data()
        ]

    def __bytes__(self):
        return b''.join(self._list())

    def __str__(self):
        return "  ".join([util.format_bytes(b) for b in self._list()])

    def _raw_data(self):
        return self.data

    @staticmethod
    def from_bytes(b):
        types = {
            1: packet.BufferSizeRequestPacket,
            2: packet.BufferSizeAllocationPacket,
            3: packet.VirtualPacket,
            4: packet.VirtualPacket,
            5: packet.AckVirtualPacket,
        }

        if b[4] not in types.keys():
            warn(f"Packet has invalid type: {b[4]}. Creating generic")
            return Packet(type=b[4], data=b[5:])

        packet_type = types[b[4]]
        return packet_type.from_bytes(b)

    @staticmethod
    def from_hex(h):
        h = h.strip()
        return Packet.from_bytes(bytes.fromhex(h))
