from ti84usb.packet import VirtualPacket
from ti84usb.types import Parameter


class ParameterDataPacket(VirtualPacket):
    type = 4
    subtype = 0x0008
    is_final = True

    params: list

    def __init__(self, params):
        if type(params) is Parameter:
            self.params = [params]
        elif type(params) is bytes:
            self.params = [Parameter.from_bytes(params)]

        elif type(params[0]) is Parameter:
            self.params = params
        elif type(params[0]) is bytes:
            self.params = [Parameter.from_bytes(b) for b in params]

    def _list(self):
        return [
            len(self)         .to_bytes(4, 'big'),
            self.type         .to_bytes(1, 'big'),
            len(self._raw_data()).to_bytes(4, 'big'),
            self.subtype      .to_bytes(2, 'big'),
            self._num_params().to_bytes(2, 'big'),
            *self._byte_params()
        ]

    def _raw_data(self):
        num_params = self._num_params().to_bytes(2, 'big')
        byte_params = b''.join(self._byte_params())
        return num_params + byte_params

    def _num_params(self):
        return len(self.params)

    def _byte_params(self):
        return [bytes(p) for p in self.params]

    @staticmethod
    def from_bytes(b):
        assert len(b) > 6, "Invalid packet: too small"  # Extra byte in header
        assert len(b) == 5 + int.from_bytes(b[0:4], 'big'), "Packet size mismatch"
        assert len(b) == 11 + int.from_bytes(b[5:9], 'big'), "Virtual packet size mismatch"

        # 0  1  2  3   4   5  6  7  8   9  10  11 12   13 14 15   16 ..
        # LL LL LL LL  TT  LL LL LL LL  TT TT  NN NN  (II II VV [ LL LL DD DD ...] ))
        num_params = int.from_bytes(b[6:8], 'big')

        params = []
        p_start = 13
        for i in range(int.from_bytes(b[11:13], 'big')):
            p_new = Parameter.from_bytes(b[p_start:])
            p_start += len(bytes(p_new))
            params += [p_new]

        return ParameterDataPacket(
            params=params
        )
