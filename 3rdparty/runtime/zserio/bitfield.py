"""
The module provides help methods for bit fields calculation.
"""

from zserio.exception import PythonRuntimeException

def getBitFieldLowerBound(length):
    """
    Gets the lower bound of a unsigned bitfield type with given length.

    :param length: Length of the unsigned bitfield in bits.
    :returns: The lowest value the unsigned bitfield can hold.
    :raises PythonRuntimeException: If unsigned bitfield with wrong length has been specified.
    """

    _checkBitFieldLength(length, MAX_UNSIGNED_BITFIELD_BITS)
    return 0

def getBitFieldUpperBound(length):

    """
    Gets the upper bound of a unsigned bitfield type with given length.

    :param length: Length of the unsigned bitfield in bits.
    :returns: The largest value the unsigned bitfield can hold.
    :raises PythonRuntimeException: If unsigned bitfield with wrong length has been specified.
    """

    _checkBitFieldLength(length, MAX_UNSIGNED_BITFIELD_BITS)
    return (1 << length) - 1

def getSignedBitFieldLowerBound(length):
    """
    Gets the lower bound of a signed bitfield type with given length.

    :param length: Length of the signed bitfield in bits.
    :returns: The lowest value the signed bitfield can hold.
    :raises PythonRuntimeException: If signed bitfield with wrong length has been specified.
    """

    _checkBitFieldLength(length, MAX_SIGNED_BITFIELD_BITS)
    return -(1 << (length - 1))

def getSignedBitFieldUpperBound(length):
    """
    Gets the upper bound of a signed bitfield type with given length.

    :param length: Length of the signed bitfield in bits.
    :returns: The largest value the signed bitfield can hold.
    :raises PythonRuntimeException: If signed bitfield with wrong length has been specified.
    """

    _checkBitFieldLength(length, MAX_SIGNED_BITFIELD_BITS)
    return (1 << (length - 1)) - 1

def _checkBitFieldLength(length, maxBitFieldLength):
    if length <= 0 or length > maxBitFieldLength:
        raise PythonRuntimeException("Asking for bound of bitfield with invalid length %d!" % length)

MAX_SIGNED_BITFIELD_BITS = 64
MAX_UNSIGNED_BITFIELD_BITS = 63
