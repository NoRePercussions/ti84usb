from ti84usb import packet
from warnings import warn


class VirtualPacket(packet.Packet):
    type: int
    subtype = None  # remove? idk allows for generics-ish
    data: bytes
    is_start: bool
    is_final: bool

    def __init__(self, data, is_start=True, is_final=True):
        self.type = 4 if is_final else 3
        self.data = data
        self.is_start = is_start
        self.is_final = is_final

    def __len__(self):
        length = len(self._raw_data())
        # Todo: ensure either both are mut.ex. or else this works
        if type(self) is VirtualPacket and self.is_start and not self.is_final:
            return length-1
        else:
            return length

    def _raw_data(self):
        return self.data

    def _list(self):
        # Test if self is not a child so children don't check params
        if type(self) is not VirtualPacket or self.is_start and self.is_final:
            return [
                len(self).to_bytes(4, 'big'),
                self.type.to_bytes(1, 'big'),
                self.subtype.to_bytes(1, 'big'),
                self._raw_data()
            ]
        else:
            return [
                len(self).to_bytes(4, 'big'),
                self.type.to_bytes(1, 'big'),
                self._raw_data()
            ]

    def __add__(self, other):
        assert isinstance(other, VirtualPacket), "Can only append with another virtual packet"
        assert not self.is_final, "Cannot append a final packet to another packet"
        assert not other.is_start, "Cannot append a packet to a start packet"

        is_complete = self.is_start and other.is_final

        # Merge raw data
        concat = self._raw_data() + other._raw_data()
        # If the new packet is a start packet,
        #   length will not include subtype
        length = len(concat)-1 if self.is_start else len(concat)

        type = b'\x04' if other.is_final else b'\x03'

        return VirtualPacket.from_bytes(
            length.to_bytes(4, 'big') + type + concat
        )

    @staticmethod
    def from_bytes(b):
        # Determine if this is a valid vpacket
        is_start = (6 + int.from_bytes(b[0:4], 'big') == len(b))
        is_final = (b[4] == 4)

        types = {
            0x0001: packet.SetModePacket,
            0x0007: packet.ParameterRequestPacket,
            0x0012: packet.AckSetModePacket,
        }

        if is_start and is_final:
            packet_type = types[b[5]]
            return packet_type.from_bytes(b)

        return VirtualPacket(b[5:], is_start=is_start, is_final=is_final)