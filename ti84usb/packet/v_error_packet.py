from ti84usb.packet import VirtualPacket

class ErrorPacket(VirtualPacket):
    type: 4
    subtype: 0xEE00

    error: bytes

    def __init__(self, error):
        self.error = error

    def _list(self):
        return [
            len(self)         .to_bytes(4, 'big'),
            self.type         .to_bytes(1, 'big'),
            len(self._raw_data()).to_bytes(4, 'big'),
            self.subtype      .to_bytes(2, 'big'),
            self.error
        ]

    def _raw_data(self):
        return self.error

    @staticmethod
    def from_bytes(b):
        assert len(b) == 5 + 6 + 2, "Packet size is wrong"

        # 0  1  2  3   4   5  6  7  8   9  10   11 12
        # LL LL LL LL  TT  LL LL LL LL  TT TT  EE EE

        return ErrorPacket(
            error=b[11:]
        )