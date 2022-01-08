from ti84usb import packet
from warnings import warn


class VirtualPacket(packet.Packet):
    type: int
    data: bytes

    def __init__(self, data, is_final=True):
        self.type = 4 if is_final else 3
        self.data = data

    def __len__(self):
        return 6 + len(self._raw_data())

    def _raw_data(self):
        return self.data

    def _list(self):
        # Test if self is not a child so children don't check params
        if type(self) is not VirtualPacket:
            return [
                len(self).to_bytes(4, 'big'),
                self.type.to_bytes(1, 'big'),
                len(self._raw_data()).to_bytes(4, 'big'),
                self.subtype.to_bytes(2, 'big'),
                self._raw_data()
            ]
        else:
            return [
                len(self._raw_data()).to_bytes(4, 'big'),
                self.type.to_bytes(1, 'big'),
                self._raw_data()
            ]

    def __add__(self, other):
        assert isinstance(other, VirtualPacket), "Can only append with another virtual packet"
        assert self.type == 0x3, "Cannot append a final packet to another packet"

        # Merge raw packet data
        concat = self._raw_data() + other._raw_data()
        # If the new packet is a start packet,
        #   length will not include subtype
        length = len(concat)

        type = other.type

        return VirtualPacket.from_bytes(
            len(concat).to_bytes(4, 'big') +
            type.to_bytes(1, 'big') +
            concat
        )

    @staticmethod
    def from_bytes(b, auto_type=True):
        # Determine if this is a valid vpacket
        is_final = (b[4] == 4)
        is_valid = is_final and (len(b)-11 == int.from_bytes(b[5:9], 'big'))

        t = int.from_bytes(b[9:11], 'big')

        types = {
            0x0001: packet.SetModePacket,

            0x0006: packet.AckEOTPacket,
            0x0007: packet.ParameterRequestPacket,
            0x0008: packet.ParameterDataPacket,
            0x0009: packet.RequestDirectoryListingPacket,
            0x000A: packet.VariableHeaderPacket,
            0x000B: packet.RequestToSendVariablePacket,

            0x0012: packet.AckSetModePacket,
            0xAA00: packet.AckDataPacket,
            0xBB00: packet.ExpectedDelayPacket,
        }

        if auto_type and is_valid and t in types:
            packet_type = types[t]
            return packet_type.from_bytes(b)

        return VirtualPacket(b[5:], is_final=is_final)
