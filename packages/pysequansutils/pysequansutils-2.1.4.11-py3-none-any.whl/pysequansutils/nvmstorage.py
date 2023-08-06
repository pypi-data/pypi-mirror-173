"""
Definititions and utilities to manage NVM data slots in  Sequans Monarch 2 platform
"""

from .status_codes import STATUS_SUCCESS, STATUS_FAILURE
from .pysequans_errors import PysequansError


# Modem NVM slots
NVM_SLOTS = range(0, 20)

# Sequans reserves slots 0-4 and 7-10. We can read these but not modify
RESERVED_NVM_SLOTS = list(range(0,5)) + list(range(7,11))

# Slots available for applications
AVAILABLE_NVM_SLOTS = [slot for slot in NVM_SLOTS if slot not in RESERVED_NVM_SLOTS]

# Data types that can be stored in NVM slots
# TODO: There is also "strid" mentioned in the manual, meaning "generic string"
NVM_CERTIFICATE = "certificate"
NVM_PRIVATE_KEY = "privatekey"
NVM_DATA_TYPES =   [NVM_CERTIFICATE, NVM_PRIVATE_KEY]

# Capacity of modem storage slots, catch excessive size before modem does
NVM_SLOT_CAPACITY = {NVM_CERTIFICATE: 8192, NVM_PRIVATE_KEY: 2048}


def nvm_read_slot(atdriver, slot, data_type):
    response = atdriver.command_response(f'AT+SQNSNVR="{data_type}",{slot}')
    print('\n'.join(response[:-1]))
    return STATUS_SUCCESS if response[-1].startswith("OK") else STATUS_FAILURE

def nvm_write_slot(atdriver, slot, data_type, data):
    # Check data size here to avoid modem failing with generic "operation not supported",
    if len(data) > NVM_SLOT_CAPACITY[data_type]:
        raise PysequansError(f"Data size {len(data)} exceeds slot capacity ({NVM_SLOT_CAPACITY[data_type]})")
    # Requiring ASCII encoding should help trap bad PEM files
    response = atdriver.write_nvm(data_type, slot, data.encode("ascii"))
    return STATUS_SUCCESS if response[-1].startswith("OK") else STATUS_FAILURE

def nvm_erase_slot(atdriver, slot, data_type):
    response = atdriver.command_response(f'AT+SQNSNVW="{data_type}",{slot},0')
    return STATUS_SUCCESS if response[-1].startswith("OK") else STATUS_FAILURE
