from ti84usb import packet, utils


class SetModePacket(packet.VirtualPacket):
    type = 4
    subtype = 0x0001

    suffix: int = (2000).to_bytes(4, 'big')
    mode_template = b'\x00\x0F\x00\x01\x00\x00'

    mode: int

    def __init__(self, mode, suffix=None):
        if type(mode) is int:
            self.mode = mode
        else:
            self.mode = mode[1]
        if suffix:
            self.suffix = suffix

    def _raw_data(self):
        temp = bytearray(self.mode_template)
        temp[1] = self.mode
        return bytes(temp) + self.suffix

    def __str__(self):
        out  = f"Set Mode Packet {id(self)}" + "\n"
        out += f"  Mode: {self._human_readable_mode()}" + "\n"
        out += f"  Suffix: {utils.format_bytes(self.suffix)}"
        return out

    def _human_readable_mode(self):
        mode_lookup_table = {
            1: "1: Startup mode",
            2: "2: Basic mode",
            3: "3: Normal mode",
        }

        if self.mode in mode_lookup_table:
            return mode_lookup_table[self.mode]
        else:
            return "Unknown mode"

    @staticmethod
    def from_bytes(b):
        assert len(b) == 5 + 6 + 10, "Invalid packet: wrong size"

        return SetModePacket(
            mode=b[11:17],
            suffix=b[17:]
        )
