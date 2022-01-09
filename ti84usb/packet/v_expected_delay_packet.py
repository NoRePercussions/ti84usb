from ti84usb import packet, utils


class ExpectedDelayPacket(packet.VirtualPacket):
    type = 4
    subtype = 0xBB00
    delay_ms: int = (2000).to_bytes(4, 'big')

    def __init__(self, delay_ms=120000):
        if delay_ms:
            self.delay_ms = delay_ms

    def _raw_data(self):
        return self.delay_ms.to_bytes(4, 'big')

    def __str__(self):
        out  = f"Expected Delay Packet {id(self)}" + "\n"
        out += f"  Delay: {self.delay_ms} ms"
        return out

    @staticmethod
    def from_bytes(b):
        assert len(b) == 5 + 6 + 4, "Invalid packet: wrong size"

        # 0  1  2  3   4   5  6  7  8   9  10  11
        # LL LL LL LL  TT  LL LL LL LL  TT TT  DD DD DD DD
        return ExpectedDelayPacket(
            delay_ms=int.from_bytes(b[11:], 'big')
        )
