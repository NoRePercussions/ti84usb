from ti84usb.packet import *
from ti84usb.types import *
from ti84usb import utils

import usb.core, usb.util
import sys
import logging


class Calculator:
    device: usb.core.Device
    read_ep: usb.core.Endpoint
    write_ep: usb.core.Endpoint

    buffer_size: int = 250

    ############################
    # Initialization functions #
    ############################

    def __init__(self, vendor_id=None, product_id=None):
        logging.debug(f"Initializing calculator")
        try:
            self._set_usb_device(vendor_id, product_id)
        except usb.core.NoBackendError as e:
            if sys.version_info[0] == 3 and sys.version_info[1] == 8:
                # python 3.8 has issues finding libusb
                raise usb.core.NoBackendError("No backend found, use a version other than 3.8") from e
            else:
                raise usb.core.NoBackendError("No backend available, make sure libusb is installed") from e

        logging.debug(f"Calculator found: {repr(self.device)}")

        self.device.set_configuration()
        self._set_endpoints()

        self.negotiate_buffer_size()

        logging.info(f"Set up {usb.util.get_string(self.device, self.device.iProduct)}: {self}")

    def _set_usb_device(self, vendor_id=None, product_id=None):
        # Manually specified calculator
        if vendor_id is not None and product_id is not None:
            calc = usb.core.find(idVendor=vendor_id, idProduct=product_id)
            if calc is not None:
                self.device = calc
                return calc
            raise ValueError(f"No calculator found with Product ID {product_id} and Vendor ID {vendor_id}")
        elif vendor_id is not None:
            calc = usb.core.find(idVendor=vendor_id)
            if calc is not None:
                self.device = calc
                return calc
            raise ValueError(f"No calculator found with Product ID {product_id}")
        elif product_id is not None:
            calc = usb.core.find(idProduct=product_id)
            if calc is not None:
                self.device = calc
                return calc
            raise ValueError(f"No calculator found with Vendor ID {vendor_id}")


        # Automatically detect a calculator
        # Ti-84 Plus
        calc = usb.core.find(idVendor=0x0451, idProduct=0xE003)
        if calc is not None:
            self.device = calc
            return calc

        # Ti-84 Plus Silver
        calc = usb.core.find(idVendor=0x0451, idProduct=0xE008)
        if calc is not None:
            self.device = calc
            return calc

        raise ValueError("No Ti-84 automatically detected")

    def _set_endpoints(self):
        cfg = self.device.get_active_configuration()
        intf = cfg[(0, 0)]

        self.read_ep = usb.util.find_descriptor(
            intf,
            custom_match=lambda e:
                usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_IN
        )
        assert self.read_ep is not None
        logging.debug(f"Read endpoint: {repr(self.read_ep)}")

        self.write_ep = usb.util.find_descriptor(
            intf,
            custom_match=lambda e:
                usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
        )
        assert self.write_ep is not None
        logging.debug(f"Write endpoint: {repr(self.write_ep)}")

    #########################
    # Read & write raw data #
    #########################

    def write_bytes(self, data, timeout_ms=None):
        logging.debug(f"Writing bytes: {utils.format_bytes(data)}")
        self.write_ep.write(data, timeout=timeout_ms)

    def write_packet(self, packet: Packet, timeout_ms=None):
        logging.debug(f"Writing packet: {repr(packet)}")
        self.write_bytes(bytes(packet), timeout_ms=timeout_ms)

        if isinstance(packet, VirtualPacket):
            try:
                ack = self.read_packet()
            except usb.core.USBTimeoutError:
                raise AssertionError("Virtual packet acknowledgement not received")
            assert isinstance(ack, AckVirtualPacket), "Virtual packet acknowledgement not received"
            logging.debug("Received virtual packet acknowledgement")

    def read_bytes(self, timeout_ms=None):
        read = bytes(self.read_ep.read(self.buffer_size, timeout=timeout_ms))
        logging.debug(f"Read bytes: {utils.format_bytes(read)}")
        return read

    def read_packet(self, timeout_ms=None):
        p = Packet.from_bytes(self.read_bytes(timeout_ms=timeout_ms))
        logging.debug(f"Read packet: {repr(p)}")

        if isinstance(p, VirtualPacket):
            logging.debug("Sending virtual packet acknowledgement")
            self.write_packet(AckVirtualPacket())
        return p

    #########################
    # Higher level routines #
    #########################

    def negotiate_buffer_size(self, buffer_size=None):
        if buffer_size is None:
            buffer_size = self.buffer_size
        logging.debug(f"Requesting buffer size {buffer_size} bytes")
        self.write_packet(BufferSizeRequestPacket(buffer_size=buffer_size))

        recv: BufferSizeAllocationPacket = self.read_packet()
        assert not isinstance(recv, ErrorPacket), f"Error received: \n{ErrorPacket}"
        self.buffer_size = recv.buffer_size
        logging.debug(f"Negotiated buffer size {self.buffer_size} bytes")

    def ping_and_set_mode(self, mode=3):
        mode_lookup_table = {
            1: "1: Startup mode",
            2: "2: Basic mode",
            3: "3: Normal mode",
        }

        if mode in mode_lookup_table:
            logging.debug(f"Setting mode {mode_lookup_table[mode]}")
        else:
            logging.debug(f"Setting unknown mode {mode}")

        self.write_packet(SetModePacket(mode))
        recv: AckSetModePacket = self.read_packet()
        assert not isinstance(recv, ErrorPacket), f"Error received: \n{ErrorPacket}"
        logging.debug(f"Mode set")


    def get_directory_listing(self, attribs='all'):
        logging.debug("Requesting directory listing")
        self.write_packet(RequestDirectoryListingPacket(attribs))

        # Recieve header packets:
        header_packets = []
        recv = None
        while not isinstance(recv, EOTPacket):
            recv = self.read_packet()
            assert not isinstance(recv, ErrorPacket), f"Error received: \n{ErrorPacket}"
            header_packets += [recv]
        return header_packets[:-1]

