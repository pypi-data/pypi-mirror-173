"""
Command handler for Sequans Monarch 2 platform NVM storage management
"""
import os
from pysequansutils.firmwareinterface import FirmwareInterface
from .atdriver import AtDriver
from .status_codes import STATUS_SUCCESS, STATUS_FAILURE
from .nvmstorage import nvm_read_slot, nvm_write_slot, nvm_erase_slot, NVM_CERTIFICATE
from .pysequans_errors import PysequansError, AtCommandError


def pem_sanity_check(data, data_type, logger):
    """
    Simple sanity check if data looks like a PEM file with given data.
    :param data: Data type to check
    :param data_type: Data type, certificate or private key
    :param logger: Logger object
    :return: Success (data looks OK) or failure
    """
    start_token = "-----BEGIN"
    end_token = "-----END"
    datatype_token = "CERTIFICATE-----" if data_type == NVM_CERTIFICATE  else "PRIVATE KEY-----"

    lines  = data.split('\n')[:-1] # Strip off empty line at end caused by expected newline at EOF

    if not (lines[0].startswith(start_token) and lines[0].endswith(datatype_token)):
        logger.debug("Bad start line: %s", lines[0])
        return STATUS_FAILURE
    if not (lines[-1].startswith(end_token) and lines[-1].endswith(datatype_token)):
        logger.debug("Bad end line: %s", lines[-1])
        return STATUS_FAILURE

    return STATUS_SUCCESS


def expand_filelist(args):
    """
    Generator for filename list. Folders are expanded, but not recursively.
    """
    for filename in args.files:
        if os.path.exists(filename):
            if os.path.isfile(filename):
                yield filename
            elif os.path.isdir(filename):
                # Yield all regular files in folder
                for f in [os.path.join(filename, f) for f in os.listdir(filename)
                          if os.path.isfile(os.path.join(filename, f))]:
                    yield f
            else:
                raise PysequansError(f"{filename} is neither regular file nor folder")
        else:
            raise PysequansError(f"File {filename} does not exist")



def nvm_cli_handler(args, logger):
    """
    Entry point for nvm command in CLI
    """
    with FirmwareInterface(port=args.port,
                           serialnumber=args.serialnumber,
                           skip_programming=args.skip_program_provision_firmware,
                           permanent_bridge=False
    ) as fwinterface:
        status = STATUS_FAILURE
        if args.data_type != NVM_CERTIFICATE and len(args.files) > 1:
            logger.error("Multiple files are only allowed for certificates")
            return STATUS_FAILURE

        with AtDriver(fwinterface=fwinterface,
                      bridge_enabled=args.skip_enter_bridgemode) as atdriver:
            try:
                atdriver.command_response("AT+CMEE=2") # We like verbose error messages
                if args.action == "read":
                    logger.info(f"Reading %s in slot %d",
                                args.data_type, args.slot)
                    status = nvm_read_slot(atdriver, args.slot, args.data_type)
                elif args.action == "write":
                    data = ""
                    for filename in expand_filelist(args):
                        logger.info("Processing file: '%s' (%u bytes) ", filename, os.path.getsize(filename))
                        with open(filename, "r") as f:
                            data += f.read()
                            if pem_sanity_check(data, args.data_type, logger) != STATUS_SUCCESS:
                                logger.error(f"Bad PEM format for '{args.data_type}' in file {filename}")
                                return STATUS_FAILURE
                    status = nvm_write_slot(atdriver, args.slot, args.data_type, data)
                    logger.info("Wrote %d bytes %s to slot %d", len(data),
                                args.data_type, args.slot)
                elif args.action == "erase":
                    logger.info("Erasing %s in slot %d",
                                args.data_type, args.slot)
                    status = nvm_erase_slot(atdriver, args.slot, args.data_type)

            except AtCommandError as e:
                if args.action in ["read", "erase"]:
                    # Modem commands fail with generic error code ("operation not supported")
                    # when trying to read or erase an empty slot. This is the same we would
                    # get if sending a non-existent command. We have to just assume that this
                    # means empty slot here, using commands known to be supported, and
                    # pre-validated parameters.
                    # FIXME: Is this an error, or should we just log info and report success?
                    logger.error("%s slot %d %s: Slot is empty", args.action.capitalize(),
                                 args.slot, args.data_type)
                    logger.debug("%s failed with %s: %s", args.action, type(e).__name__, e)
                else:
                    logger.error("%s failed with %s: %s", args.action.capitalize(),
                                 type(e).__name__, e)
                status = STATUS_FAILURE

            except Exception as e:
                # Catch other possible failures
                logger.error("%s %s slot %d failed with %s: %s",  args.action.capitalize(),
                             args.data_type, args.slot, type(e).__name__, e)
                status = STATUS_FAILURE

        return status
