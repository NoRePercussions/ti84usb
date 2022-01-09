from ti84usb.packet import VirtualPacket


class ParameterRequestPacket(VirtualPacket):
    type = 4
    subtype = 0x0007

    params: list

    def __init__(self, params):
        if type(params) is not list:
            self.params = [params]
        elif type(params[0]) is int:
            self.params = params
        else:
            self.params = [int.from_bytes(b, 'big') for b in params]

    def _list(self):
        return [
            len(self)         .to_bytes(4, 'big'),
            self.type         .to_bytes(1, 'big'),
            len(self._raw_data()).to_bytes(4, 'big'),
            self.subtype      .to_bytes(2, 'big'),
            self._num_params().to_bytes(2, 'big'),
            b''.join(self._byte_params())
        ]

    def _raw_data(self):
        num_params = self._num_params().to_bytes(2, 'big')
        byte_params = b''.join(self._byte_params())
        return num_params + byte_params

    def _num_params(self):
        return len(self.params)

    def _byte_params(self):
        return [p.to_bytes(2, 'big') for p in self.params]

    def __str__(self):
        out   = f"Parameter Data Packet {id(self)}" + "\n"
        out  += f"  Parameters: {self.params}"
        return out


    @staticmethod
    def from_bytes(b):
        assert len(b) > 6, "Invalid packet: too small"  # Extra byte in header
        assert len(b) == 5 + int.from_bytes(b[0:4], 'big'), "Packet size mismatch"
        assert len(b) == 11 + int.from_bytes(b[5:9], 'big'), "Packet size mismatch"

        # 0  1  2  3   4   5  6  7  8   9 10   11 12  13 14  15 16
        # LL LL LL LL  TT  LL LL LL LL  TT TT  NN NN  II II  II II ...
        num_params = int.from_bytes(b[11:13], 'big')
        params = [b[i:i+2] for i in range(13, 13 + 2*num_params, 2)]
        return ParameterRequestPacket(
            params=params
        )
