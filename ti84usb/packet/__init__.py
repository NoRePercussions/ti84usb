from .packet import Packet
from .r_buffer_size_request_packet import BufferSizeRequestPacket
from .r_buffer_size_allocation_packet import BufferSizeAllocationPacket
from .r_virtual_packet import VirtualPacket
from .r_ack_virtual_packet import AckVirtualPacket

# Virtual Packet Subtypes
from .v_set_mode_packet import SetModePacket
# 0x0002 \
# 0x0003 | Probably won't be implemented soon:
# 0x0004 |     OS data is harder to handle
# 0x0005 /
from .v_ack_EOT_packet import AckEOTPacket
from .v_parameter_request_packet import ParameterRequestPacket
from .v_parameter_data_packet import ParameterDataPacket
from .v_request_directory_listing import RequestDirectoryListingPacket
from .v_variable_header_packet import VariableHeaderPacket
from .v_request_to_send_variable import RequestToSendVariablePacket
# 0x000C
from .v_variable_content_packet import VariableContentPacket
from .v_set_parameter_packet import SetParameterPacket
# 0x0010
# 0x0011
from .v_ack_set_mode_packet import AckSetModePacket
from .v_ack_data_packet import AckDataPacket
from .v_expected_delay_packet import ExpectedDelayPacket
# 0xDD00
from .v_error_packet import ErrorPacket
