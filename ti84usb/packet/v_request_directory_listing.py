from ti84usb.packet import VirtualPacket


class RequestDirectoryListingPacket(VirtualPacket):
    type = 4
    subtype = 0x0009

    attribs: list
    constant = b'\x00\x01\x00\x01\x00\x01\x01'

    def __init__(self, attribs):
        if type(attribs) is not list:
            self.attribs = [attribs]
        elif type(attribs[0]) is int:
            self.attribs = attribs
        else:
            self.attribs = [int.from_bytes(b, 'big') for b in attribs]

    def _list(self):
        return [
            len(self)         .to_bytes(4, 'big'),
            self.type         .to_bytes(1, 'big'),
            len(self._raw_data()).to_bytes(4, 'big'),
            self.subtype      .to_bytes(2, 'big'),
            self._num_params().to_bytes(4, 'big'),
            b''.join(self._byte_params()),
            self.constant
        ]

    def _raw_data(self):
        num_params = self._num_params().to_bytes(4, 'big')
        byte_params = b''.join(self._byte_params())
        return num_params + byte_params + self.constant

    def _num_params(self):
        return len(self.attribs)

    def _byte_params(self):
        return [p.to_bytes(2, 'big') for p in self.attribs]

    @staticmethod
    def from_bytes(b):
        assert len(b) > 6, "Invalid packet: too small"  # Extra byte in header
        assert len(b) == 5 + int.from_bytes(b[0:4], 'big'), "Packet size mismatch"
        assert len(b) == 11 + int.from_bytes(b[5:9], 'big'), "Packet size mismatch"

        # 0  1  2  3   4   5  6  7  8   9 10   11 12 13 14  15 16  17 18
        # LL LL LL LL  TT  LL LL LL LL  TT TT  NN NN NN NN  II II  II II ...
        num_params = int.from_bytes(b[11:15], 'big')
        attribs = [b[i:i+2] for i in range(15, 15 + 4*num_params, 4)]
        return RequestDirectoryListingPacket(
            attribs=attribs
        )
