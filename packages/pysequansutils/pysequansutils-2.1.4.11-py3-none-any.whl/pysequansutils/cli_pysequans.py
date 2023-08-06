"""
pysequansutils CLI: "pysequans"
"""
import sys
import logging
import argparse
import os
import textwrap

from logging import getLogger
from logging.config import dictConfig
from appdirs import user_log_dir
import yaml
from yaml.scanner import ScannerError
from pykitcommander.kitcommandererrors import KitConnectionError

from .status_codes import STATUS_SUCCESS, STATUS_FAILURE
from .cli_upgrade_main import upgrade_cli_handler
from .upgrade import BUNDLED_FW_VERSION
from .upgrade import prompt_for_license_agreement_acceptance
from .nvmstorage import NVM_SLOTS, AVAILABLE_NVM_SLOTS, NVM_CERTIFICATE, NVM_PRIVATE_KEY
from .cli_nvm_main import nvm_cli_handler

try:
    #pylint: disable=no-name-in-module
    from .version import VERSION, BUILD_DATE, COMMIT_ID
except ImportError:
    print("Version info not found!")
    VERSION = "0.0.0"
    COMMIT_ID = "N/A"
    BUILD_DATE = "N/A"

def print_kit_status(error):
    """
    Print details from KitConnectionError exception due to none or too many kits
    matching serial number specification (if any)

    :param error: KitConnectionError exception object
    :type error: :class `pykitcommander.kitcommandererrors.KitConnectionError` object
    """
    # There must be exactly one tool connected, or user must disambiguate with (partial)
    # serial number
    logger = getLogger(__name__)
    if not error.value:
        logger.error("No suitable kits found")
    elif len(error.value) > 1:
        logger.error("Multiple kits found.")
        logger.error("Please specify serial number ending digits for the one you want")
        for tool in error.value:
            logger.error("Tool: %s Serial: %s Device: %s",
                         tool["product"][:16],
                         tool["serial"][:20],
                         tool["device_name"])
    else:
        # If exactly one was found, something is wrong with it, expect reason in msg
        tool = error.value[0]
        logger.error("Tool: %s Serial: %s Device: %s: %s",
                     tool["product"][:16],
                     tool["serial"][:20],
                     tool["device_name"],
                     error.msg)

def setup_logging(user_requested_level=logging.WARNING, default_path='logging.yaml',
                  env_key='MICROCHIP_PYTHONTOOLS_CONFIG'):
    """
    Setup logging configuration for this CLI

    :param user_requested_level: Logging level requested
    :type user_requested_level: int log level as defined by logging module
    :param default_path: Default path to logging configuration YAML file.  This one will be used unless a different
        path is specified through the environment variable given by env_key.
    :type default_path: str
    :param env_key: Name of environment variable that can be used to override the default logging configuration YAML
        file path
    :type env_key: str
    """
    # Logging config YAML file can be specified via environment variable
    value = os.getenv(env_key, None)
    if value:
        path = value
    else:
        # Otherwise use the one shipped with this application
        path = os.path.join(os.path.dirname(__file__), default_path)
    # Load the YAML if possible
    if os.path.exists(path):
        try:
            with open(path, 'rt', encoding="UTF-8") as file:
                # Load logging configfile from yaml
                configfile = yaml.safe_load(file)
                # File logging goes to user log directory under Microchip/modulename
                logdir = user_log_dir(__name__, "Microchip")
                # Look through all handlers, and prepend log directory to redirect all file loggers
                num_file_handlers = 0
                for handler in configfile['handlers'].keys():
                    # A filename key
                    if 'filename' in configfile['handlers'][handler].keys():
                        configfile['handlers'][handler]['filename'] = os.path.join(
                            logdir, configfile['handlers'][handler]['filename'])
                        num_file_handlers += 1
                if num_file_handlers > 0:
                    # Create it if it does not exist
                    os.makedirs(logdir, exist_ok=True)

                if user_requested_level <= logging.DEBUG:
                    # Using a different handler for DEBUG level logging to be able to have a more detailed formatter
                    configfile['root']['handlers'].append('console_detailed')
                    # Remove the original console handlers
                    try:
                        configfile['root']['handlers'].remove('console_only_info')
                    except ValueError:
                        # The yaml file might have been customized and the console_only_info handler might
                        # already have been removed
                        pass
                    try:
                        configfile['root']['handlers'].remove('console_not_info')
                    except ValueError:
                        # The yaml file might have been customized and the console_only_info handler might
                        # already have been removed
                        pass
                else:
                    # Console logging takes granularity argument from CLI user
                    configfile['handlers']['console_only_info']['level'] = user_requested_level
                    configfile['handlers']['console_not_info']['level'] = user_requested_level

                # Root logger must be the most verbose of the ALL YAML configurations and the CLI user argument
                most_verbose_logging = min(user_requested_level, getattr(logging, configfile['root']['level']))
                for handler in configfile['handlers'].keys():
                    # A filename key
                    if 'filename' in configfile['handlers'][handler].keys():
                        level = getattr(logging, configfile['handlers'][handler]['level'])
                        most_verbose_logging = min(most_verbose_logging, level)
                configfile['root']['level'] = most_verbose_logging
            dictConfig(configfile)
            return
        except ScannerError:
            # Error while parsing YAML
            print(f"Error parsing logging config file '{path}'")
        except KeyError as keyerror:
            # Error looking for custom fields in YAML
            print(f"Key {keyerror} not found in logging config file")
    else:
        # Config specified by environment variable not found
        print(f"Unable to open logging config file '{path}'")

    # If all else fails, revert to basic logging at specified level for this application
    print("Reverting to basic logging.")
    logging.basicConfig(level=user_requested_level)

def main():
    """
    Entrypoint for installable CLI

    Configures the top-level CLI and parses the arguments
    """

    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter,
        description=textwrap.dedent('''\
    pysequans: a command line interface for Microchip pysequansutils

    basic usage:
        - pysequans [-common-switches] <command> <action> [-switches]
            '''),
        epilog=textwrap.dedent(f'''usage examples:
    Upgrade command
        Do a full upgrade of Sequans Monarch 2 platform to version {BUNDLED_FW_VERSION}
        The upgrade will be skipped if the Monarch 2 platform firmware already is up to date,
        i.e.  version number of currently running firmware >= {BUNDLED_FW_VERSION}
        - pysequans upgrade full

        Do a forced full upgrade/downgrade of Sequans Monarch 2 platform, disregarding the version check
        - pysequans upgrade full --force

        Do a full upgrade, but using dedicated bridge firmware already programmed in target
        - pysequans upgrade full --sprov --sbridge

        Do a full upgrade, but use a specified dup file instead of the bundled firmware file
        Note that this option will not do any version checking
        The Sequans Monarch 2 platform will always be programmed with the provided firmware
        - pysequans upgrade full --firmware my_firmware.dup

    NVM storage management command
        Write certificate in file 'mycert.crt' to NVM slot 18
        - pysequans nvm  write 18 --certificate -f cert.crt

        Concatenate all certificates in a folder and write to NVM slot 17
        - pysequans nvm  write 17 --certificate -f my_cert_folder

        Concatenate multiple certificate files and write to NVM slot 16
        - pysequans nvm  write 16 --certificate -f cert1.crt -f cert2.crt -f cert3.crt

        Erase private key in slot 11
        - pysequans nvm erase 11 --privatekey

        Read certificate in slot 18
        - pysequans nvm read 18 --certificate
        '''))

    # Global switches that are all "do X and exit"
    parser.add_argument("-V", "--version", action="store_true",
                        help="Print pysequans version number and exit")

    parser.add_argument("-R", "--release-info", action="store_true",
                        help="Print pysequans release details and exit")

    # Global switches that are common to all commands
    parser.add_argument("-v", "--verbose",
                        default="info",
                        choices=['debug', 'info', 'warning', 'error', 'critical'],
                        help="Logging verbosity/severity level")

    parser.add_argument("-s", "--serialnumber",
                        type=str,
                        help="USB serial number of the kit to use\n"
                        "This is optional if only one kit is connected\n"
                        "Sub-string matching on end of serial number is supported")

    parser.add_argument("-sprov", "--skip-program-provision-firmware", action="store_true",
              help="Skip programming provisioning firmware.\n"
             "Setting this option indicates that the target already is programmed with provisioning firmware or\n"
             "a permanent bridge, in which case the --skip-enter-bridge switch should also be enabled.\n"
             "NOTE: This is an advanced option and may break the process")

    parser.add_argument("-sbridge", "--skip-enter-bridgemode",
        action="store_true", dest="skip_enter_bridgemode",
        help="Skip command to enable bridge mode in target firmware.\n"
             "Setting this option indicates that the target is programmed with permanent bridge firmware\n"
             "NOTE: This is an advanced option and may break the process")

    parser.add_argument("-P", "--port",
                        type=str, default=None,
                        help="Serial port name for communication with kit")

    # First 'argument' is the command, which is a sub-parser
    subparsers = parser.add_subparsers(
        title='commands',
        dest='command',
        description="use one and only one of these commands",
        help="for additional help use pysequans <command> --help")

    # Make the command required but not for -V or -R arguments
    subparsers.required = not any(arg in ["-V", "--version", "-R", "--release-info"] for arg in sys.argv)

    # Upgrade command
    upgrade_command = subparsers.add_parser(
        name='upgrade',
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(
            prog, max_help_position=0, width=80),
        help='functions related to Sequans Monarch 2 platform firmware upgrade')

    upgrade_command.add_argument(
        'action',
        help=(f'''
\nupgrade actions:
- full: does a full firmware upgrade of Monarch 2 platform
    Default is to upgrade to version {BUNDLED_FW_VERSION} using bundled firmware
- report: read and report Monarch 2 platform firmware version
'''),
                                 choices=['full', 'report'])

    upgrade_command.add_argument(
        "-f", "--force", action="store_true",
        help="Force upgrade/downgrade, i.e. disregard version of currently loaded firmware\n"
        "This option is ignored when a specific firmware file is configured using the --firmware argument")

    upgrade_command.add_argument("-fw", "--firmware", type=str,
        help="Sequans Monarch 2 platform firmware (dup file)\n"
        f"Optional, if not specified the bundled firmware (version {BUNDLED_FW_VERSION}) will be used\n"
        "When this argument is used no version check is performed,\n"
        "i.e. the Monarch 2 platform will always be programmed with the specified firmware file",
        dest="firmware")

    upgrade_command.add_argument(
        "-r", "--report", action="store_true",
        help="Just read and report Sequans Monarch 2 platform firmware version\n"
        "No upgrade will be done")

    # Modem NVM storage management command
    nvm_command = subparsers.add_parser(
        name='nvm',
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(
            prog, max_help_position=0, width=80),
        help='Read/write/erase content in Sequans Monarch 2 platform NVM storage slots')

    nvm_command.add_argument(
        'action',
        choices=['write', 'erase', 'read'],
        help=('''
\nactions:
- write: Upload data from file into Monarch 2 NVM storage slot
- erase: Erase data in Monarch 2 NVM storage slot
- read:  Read data in Monarch 2 NVM storage slot\n
'''))

    nvm_command.add_argument(
        "slot", type=int,
        choices=NVM_SLOTS  if "read" in sys.argv else AVAILABLE_NVM_SLOTS,
        help="NVM slot number")

    nvm_command.add_argument(
        "-f", "--file", type=str, default=[], action="append",
        required="write" in sys.argv, dest="files",
        help="PEM format certificate or private key file to upload,"
        " or folder containing certificate files."
        " Can be repeated. Multiple files only allowed for certificates")

    # The mutually exclusive group below will enforce exactly one of the --certificate
    # or --privatekey data type options, and const value stored in data_type in either case.
    # This is preferred over a positional argument with choices list because options
    # can be abbreviated (--certificate, --cert and -c are equivalent), and allows more
    # flexibility when it comes to CLI argument order.
    datatype_opts = nvm_command.add_mutually_exclusive_group(required=True)
    datatype_opts.add_argument(
        "-c", "--certificate", action="store_const", const=NVM_CERTIFICATE,
        dest ="data_type", help="Access certificate NVM storage")

    datatype_opts.add_argument(
        "-p", "--private-key", action="store_const", const=NVM_PRIVATE_KEY,
        dest="data_type", help="Access private key NVM storage")

    # Parse
    args = parser.parse_args()

    # Setup logging
    setup_logging(user_requested_level=getattr(logging, args.verbose.upper()))
    logger = logging.getLogger(__name__)

    # Dispatch
    if args.version or args.release_info:
        print(f"pysequansutils version {VERSION}")
        if args.release_info:
            print(f"Build date:  {BUILD_DATE}")
            print(f"Commit ID:   {COMMIT_ID}")
            print(f"Installed in {os.path.abspath(os.path.dirname(__file__))}")
        return STATUS_SUCCESS

    if args.skip_enter_bridgemode and not args.skip_program_provision_firmware:
        print("ERROR - Argument mismatch: Provisioning firmware requires bridge mode command so\n"
              "if using --skip-enter-bridge then --skip-program-provision-firmware must also be used.\n"
              "In other words the target must be programmed with permanent bridge upfront")
        return STATUS_FAILURE

    try:
        if args.command == "upgrade":
            # Upgrading to new firmware requires acceptance of the Sequans license agreement
            if not prompt_for_license_agreement_acceptance():
                return STATUS_FAILURE
            return upgrade_cli_handler(args)
        elif args.command == "nvm":
            return nvm_cli_handler(args, logger)
    except KitConnectionError as connection_error:
        print_kit_status(connection_error)
        return STATUS_FAILURE
    except Exception as exc:
        logger.error("Operation failed with %s: %s", type(exc).__name__, exc)
        logger.debug(exc, exc_info=True)    # get traceback if debug loglevel

    return STATUS_FAILURE

if __name__ == "__main__":
    sys.exit(main())
