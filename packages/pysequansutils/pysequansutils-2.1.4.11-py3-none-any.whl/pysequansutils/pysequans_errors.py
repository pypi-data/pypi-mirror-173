"""
Exceptions/Errors that pysequansutils can raise
Application can catch PysequansError to catch all these exceptions, or
one of its sub-classes for finer granularity error handling.
"""

class PysequansError(Exception):
    """
    Base class for all pysequansutils specific exceptions

    :param msg: Error message
    :type msg: str
    :param code: Error code
    :type code: int
    """
    def __init__(self, msg=None, code=0):
        super().__init__(msg)
        self.code = code

class AtCommandError(PysequansError):
    """
    Error used when AT modem command fails (modem reports ERROR)

    :param msg: Error message
    :type msg: str
    :param code: Error code
    :type code: int
    """

class PysequansMinVersionError(PysequansError):
    """
    Error used when current Sequans Monarch 2 firmware version is below minimum version to ensure safe upgrade

    :param msg: Error message
    :type msg: str
    :param code: Error code
    :type code: int
    """
