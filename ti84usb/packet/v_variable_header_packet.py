from ti84usb.packet import VirtualPacket
from ti84usb.types import Attribute


class VariableHeaderPacket(VirtualPacket):
    type = 4
    subtype = 0x000A

    name: str
    attribs: list

    def __init__(self, name, attribs=None):
        self.name = name

        if type(attribs) is Attribute:
            self.attribs = [attribs]
        elif type(attribs) is bytes:
            self.attribs = [Attribute.from_bytes(attribs)]
        # Or, if it is listlike
        elif isinstance(attribs, list) and type(attribs[0]) is Attribute:
            self.attribs = attribs
        elif isinstance(attribs, list) and type(attribs[0]) is bytes:
            self.attribs = [Attribute.from_bytes(b) for b in attribs]

    def _list(self):
        return [
            len(self)         .to_bytes(4, 'big'),
            self.type         .to_bytes(1, 'big'),
            len(self._raw_data()).to_bytes(4, 'big'),
            self.subtype      .to_bytes(2, 'big'),
            len(self.name).to_bytes(2, 'big'),
            self.name.encode('ascii'), b'\x00',
            self._num_attribs().to_bytes(2, 'big'),
            *self._byte_attribs()
        ]

    def _raw_data(self):
        out = len(self.name).to_bytes(2, 'big')
        out += self.name.encode('ascii') + b'\x00'

        num_params = self._num_attribs()
        out += num_params.to_bytes(2, 'big')
        if num_params > 0:
            out += b''.join(self._byte_attribs())
        return out

    def _num_attribs(self):
        return len(self.attribs)

    def _byte_attribs(self):
        return [bytes(a) for a in self.attribs]

    def __str__(self):
        out  = f"Variable Header Packet {id(self)}" + "\n"
        out += f"  Name: {self.name}" + "\n"
        out += f"  Attributes:"
        for a in self.attribs:
            if a.is_valid:
                out += f"\n    {a.id}: 0x{a.data.hex()}"
            else:
                out += f"\n    {a.id}: Invalid"
        return out

    @staticmethod
    def from_bytes(b):
        assert len(b) > 6, "Invalid packet: too small"  # Extra byte in header
        assert len(b) == 5 + int.from_bytes(b[0:4], 'big'), "Packet size mismatch"
        assert len(b) == 11 + int.from_bytes(b[5:9], 'big'), "Virtual packet size mismatch"

        # 0  1  2  3   4   5  6  7  8   9  10  11 12 13    14  15  16 17   18..
        # LL LL LL LL  TT  LL LL LL LL  TT TT  LL?LL NN NN... 00  NN NN (II II VV [ LL LL DD DD ...] ))

        name_end = 14 + int.from_bytes(b[11:13], 'big')
        name = b[13:name_end-1].decode("ascii")

        num_attribs = int.from_bytes(b[name_end:name_end+2], 'big')
        attribs = []
        a_start = name_end + 2
        for i in range(num_attribs):
            a_new = Attribute.from_bytes(b[a_start:])
            a_start += len(bytes(a_new))
            attribs += [a_new]

        return VariableHeaderPacket(
            name=name,
            attribs=attribs
        )
