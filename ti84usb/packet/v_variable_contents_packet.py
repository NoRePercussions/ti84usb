from ti84usb import packet, utils


class VariableContentsPacket(packet.VirtualPacket):
    type = 4
    subtype = 0x0009

    data: bytes

    def __init__(self, data):
        self.data = data

    def __str__(self):
        out  = f"Variable Content Packet {id(self)}" + "\n"
        out += f"  Data: {utils.format_bytes(self.data)}"
        return out
