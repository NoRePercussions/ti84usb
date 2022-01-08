from ti84usb.packet import VirtualPacket


class VariableContentsPacket(VirtualPacket):
    type = 4
    subtype = 0x0009

    data: bytes

    def __init__(self, data):
        self.data = data
