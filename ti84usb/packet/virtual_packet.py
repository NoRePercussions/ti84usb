from ti84usb import packet
from warnings import warn


class VirtualPacket(packet.Packet):
    type: int
    subtype: int
    data: bytes
    is_final: bool

    def __init__(self, subtype, data, is_final=False):
        self.type = 4 if is_final else 3
        self.subtype = subtype
        self.data = data
        self.is_final = is_final

    def _raw_data(self):
        return self.data

    def _list(self):
        return [
            len(self)   .to_bytes(4, 'big'),
            self.type   .to_bytes(1, 'big'),
            self.subtype.to_bytes(1, 'big'),
            self._raw_data()
        ]

    def __add__(self, other):
        assert not self.is_final, "Cannot add on after final frame"
        assert self.subtype == other.subtype, "Subtypes do not match"

        return VirtualPacket(
            self.subtype,
            self.data + other.data,
            other.is_final
        )

    @staticmethod
    def from_bytes(b):
        assert len(b) > 6, "Invalid packet: too small"  # Extra byte in header
        assert len(b) == 6 + int.from_bytes(b[0:4], 'big'), "Packet size mismatch"

        types = {
            1: packet.SetModePacket,
        }

        if b[5] not in types.keys():
            warn(f"Virtual packet has invalid subtype: {b[5]}. Creating generic")
            return VirtualPacket(
                subtype=b[5],
                data=b[6:],
                is_final=(b[4] == 4)
            )

        packet_type = types[b[5]]

        return packet_type.from_bytes(b)
