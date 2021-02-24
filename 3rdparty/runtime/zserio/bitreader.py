"""
The module implements abstraction for reading data to the bit stream.
"""

import typing

from zserio.bitbuffer import BitBuffer
from zserio.limits import INT64_MIN
from zserio.exception import PythonRuntimeException
from zserio.float import convertUInt16ToFloat, convertUInt32ToFloat, convertUInt64ToFloat

class BitStreamReader:
    """
    Bit stream reader.
    """

    def __init__(self, buffer: bytes, bitSize: typing.Optional[int] = None) -> None:
        """
        Constructs bit stream reader from bytes buffer.

        Because bit buffer size does not have to be byte aligned (divisible by 8), it's possible that not all
        bits of the last byte are used. In this case, only most significant bits of the corresponded size are
        used.

        :param buffer: Bytes-like buffer to read as a bit stream.
        :param bitSize: Number of bits stored in buffer to use.
        :raises PythonRuntimeException: If bitSize is out of range.
        """

        self._bitBuffer: BitBuffer = BitBuffer(buffer, bitSize)
        self._bitPosition: int = 0

    @classmethod
    def fromBitBuffer(cls: typing.Type['BitStreamReader'], bitBuffer: BitBuffer) -> 'BitStreamReader':
        """
        Constructs bit stream reader from bit buffer.

        :param bitBuffer: Bit buffer to read as a bit stream.
        """

        instance = cls(bitBuffer.getBuffer(), bitBuffer.getBitSize())

        return instance

    @classmethod
    def fromFile(cls: typing.Type['BitStreamReader'], filename: str) -> 'BitStreamReader':
        """
        Constructs bit stream reader from file.

        :param filename: Filename to read as a bit stream.
        """

        with open(filename, 'rb') as file:
            return cls(file.read())

    def readBits(self, numBits: int) -> int:
        """
        Reads given number of bits from the bit stream as an unsigned integer.

        :param numBits: Number of bits to read.
        :returns: Read bits as an unsigned integer.
        :raises PythonRuntimeException: If the numBits is invalid number of the reading goes behind the stream.
        """

        if numBits < 0:
            raise PythonRuntimeException("BitStreamReader: Reading negative number of bits!")

        endBitPosition = self._bitPosition + numBits

        if endBitPosition > self._bitBuffer.getBitSize():
            raise PythonRuntimeException("BitStreamReader: Reading behind the stream!")

        startByte = self._bitPosition // 8
        endByte = (endBitPosition - 1) // 8

        buffer = self._bitBuffer.getBuffer()
        value = int.from_bytes(buffer[startByte : endByte + 1], byteorder='big', signed=False)

        lastBits = endBitPosition % 8
        if lastBits != 0:
            value >>= (8 - lastBits)
        value &= (1 << numBits) - 1

        self._bitPosition = endBitPosition

        return value

    def readSignedBits(self, numBits: int) -> int:
        """
        Reads given number of bits from the bit stream as a signed integer.

        :param numBits: Number of bits to read
        :returns: Read bits as a signed integer.
        :raises PythonRuntimeException: If the numBits is invalid number of the reading goes behind the stream.
        """

        value = self.readBits(numBits)

        if numBits != 0 and (value >> (numBits - 1)) != 0:
            # signed
            return value - (1 << numBits)
        else:
            # unsigned
            return value

    def readVarInt16(self) -> int:
        """
        Reads variable 16-bit signed integer value from the bit stream.

        :returns: Variable 16-bit signed integer value.
        """

        byte = self.readBits(8) # byte 1
        sign = byte & VARINT_SIGN_1
        result = byte & VARINT_BYTE_1
        if byte & VARINT_HAS_NEXT_1 == 0:
            return -result if sign != 0 else result

        result = (result << 8) | self.readBits(8) # byte 2
        return -result if sign else result

    def readVarInt32(self) -> int:
        """
        Reads variable 32-bit signed integer value from the bit stream.

        :returns: Variable 32-bit signed integer value.
        """

        byte = self.readBits(8) # byte 1
        sign = byte & VARINT_SIGN_1
        result = byte & VARINT_BYTE_1
        if byte & VARINT_HAS_NEXT_1 == 0:
            return -result if sign else result

        byte = self.readBits(8) # byte 2
        result = result << 7 | (byte & VARINT_BYTE_N)
        if byte & VARINT_HAS_NEXT_N == 0:
            return -result if sign else result

        byte = self.readBits(8) # byte 3
        result = result << 7 | (byte & VARINT_BYTE_N)
        if byte & VARINT_HAS_NEXT_N == 0:
            return -result if sign else result

        result = result << 8 | self.readBits(8) # byte 4
        return -result if sign else result

    def readVarInt64(self) -> int:
        """
        Reads variable 64-bit signed integer value from the bit stream.

        :returns: Variable 64-bit signed integer value.
        """

        byte = self.readBits(8) # byte 1
        sign = byte & VARINT_SIGN_1
        result = byte & VARINT_BYTE_1
        if byte & VARINT_HAS_NEXT_1 == 0:
            return -result if sign else result

        byte = self.readBits(8) # byte 2
        result = result << 7 | (byte & VARINT_BYTE_N)
        if byte & VARINT_HAS_NEXT_N == 0:
            return -result if sign else result

        byte = self.readBits(8) # byte 3
        result = result << 7 | (byte & VARINT_BYTE_N)
        if byte & VARINT_HAS_NEXT_N == 0:
            return -result if sign else result

        byte = self.readBits(8) # byte 4
        result = result << 7 | (byte & VARINT_BYTE_N)
        if byte & VARINT_HAS_NEXT_N == 0:
            return -result if sign else result

        byte = self.readBits(8) # byte 5
        result = result << 7 | (byte & VARINT_BYTE_N)
        if byte & VARINT_HAS_NEXT_N == 0:
            return -result if sign else result

        byte = self.readBits(8) # byte 6
        result = result << 7 | (byte & VARINT_BYTE_N)
        if byte & VARINT_HAS_NEXT_N == 0:
            return -result if sign else result

        byte = self.readBits(8) # byte 7
        result = result << 7 | (byte & VARINT_BYTE_N)
        if byte & VARINT_HAS_NEXT_N == 0:
            return -result if sign else result

        result = result << 8 | self.readBits(8) # byte 8
        return -result if sign else result

    def readVarInt(self) -> int:
        """
        Reads variable signed integer value (up to 9 bytes) from the bit stream.

        :returns: Variable signed integer value (up to 9 bytes).
        """

        byte = self.readBits(8) # byte 1
        sign = byte & VARINT_SIGN_1
        result = byte & VARINT_BYTE_1
        if byte & VARINT_HAS_NEXT_1 == 0:
            return (INT64_MIN if result == 0 else -result) if sign else result

        byte = self.readBits(8) # byte 2
        result = result << 7 | (byte & VARINT_BYTE_N)
        if byte & VARINT_HAS_NEXT_N == 0:
            return -result if sign else result

        byte = self.readBits(8) # byte 3
        result = result << 7 | (byte & VARINT_BYTE_N)
        if byte & VARINT_HAS_NEXT_N == 0:
            return -result if sign else result

        byte = self.readBits(8) # byte 4
        result = result << 7 | (byte & VARINT_BYTE_N)
        if byte & VARINT_HAS_NEXT_N == 0:
            return -result if sign else result

        byte = self.readBits(8) # byte 5
        result = result << 7 | (byte & VARINT_BYTE_N)
        if byte & VARINT_HAS_NEXT_N == 0:
            return -result if sign else result

        byte = self.readBits(8) # byte 6
        result = result << 7 | (byte & VARINT_BYTE_N)
        if byte & VARINT_HAS_NEXT_N == 0:
            return -result if sign else result

        byte = self.readBits(8) # byte 7
        result = result << 7 | (byte & VARINT_BYTE_N)
        if byte & VARINT_HAS_NEXT_N == 0:
            return -result if sign else result

        byte = self.readBits(8) # byte 8
        result = result << 7 | (byte & VARINT_BYTE_N)
        if byte & VARINT_HAS_NEXT_N == 0:
            return -result if sign else result

        result = result << 8 | self.readBits(8) # byte 9
        return -result if sign else result

    def readVarUInt16(self) -> int:
        """
        Reads variable 16-bit unsigned integer value from the bit stream.

        :returns: Variable 16-bit unsigned integer value.
        """

        byte = self.readBits(8) # byte 1
        result = byte & VARUINT_BYTE
        if byte & VARUINT_HAS_NEXT == 0:
            return result

        result = result << 8 | self.readBits(8) # byte 2
        return result

    def readVarUInt32(self) -> int:
        """
        Reads variable 32-bit unsigned integer value from the bit stream.

        :returns: Variable 32-bit unsigned integer value.
        """

        byte = self.readBits(8) # byte 1
        result = byte & VARUINT_BYTE
        if byte & VARUINT_HAS_NEXT == 0:
            return result

        byte = self.readBits(8) # byte 2
        result = result << 7 | (byte & VARUINT_BYTE)
        if byte & VARUINT_HAS_NEXT == 0:
            return result

        byte = self.readBits(8) # byte 3
        result = result << 7 | (byte & VARUINT_BYTE)
        if byte & VARUINT_HAS_NEXT == 0:
            return result

        result = result << 8 | self.readBits(8) # byte 4
        return result

    def readVarUInt64(self) -> int:
        """
        Reads variable 64-bit unsigned integer value from the bit stream.

        :returns: Variable 64-bit unsigned integer value.
        """

        byte = self.readBits(8) # byte 1
        result = byte & VARUINT_BYTE
        if byte & VARUINT_HAS_NEXT == 0:
            return result

        byte = self.readBits(8) # byte 2
        result = result << 7 | (byte & VARUINT_BYTE)
        if byte & VARUINT_HAS_NEXT == 0:
            return result

        byte = self.readBits(8) # byte 3
        result = result << 7 | (byte & VARUINT_BYTE)
        if byte & VARUINT_HAS_NEXT == 0:
            return result

        byte = self.readBits(8) # byte 4
        result = result << 7 | (byte & VARUINT_BYTE)
        if byte & VARUINT_HAS_NEXT == 0:
            return result

        byte = self.readBits(8) # byte 5
        result = result << 7 | (byte & VARUINT_BYTE)
        if byte & VARUINT_HAS_NEXT == 0:
            return result

        byte = self.readBits(8) # byte 6
        result = result << 7 | (byte & VARUINT_BYTE)
        if byte & VARUINT_HAS_NEXT == 0:
            return result

        byte = self.readBits(8) # byte 7
        result = result << 7 | (byte & VARUINT_BYTE)
        if byte & VARUINT_HAS_NEXT == 0:
            return result

        result = result << 8 | self.readBits(8) # byte 8
        return result

    def readVarUInt(self) -> int:
        """
        Reads variable unsigned integer value (up to 9 bytes) from the bit stream.

        :returns: Variable unsigned integer value (up to 9 bytes).
        """

        byte = self.readBits(8) # byte 1
        result = byte & VARUINT_BYTE
        if byte & VARUINT_HAS_NEXT == 0:
            return result

        byte = self.readBits(8) # byte 2
        result = result << 7 | (byte & VARUINT_BYTE)
        if byte & VARUINT_HAS_NEXT == 0:
            return result

        byte = self.readBits(8) # byte 3
        result = result << 7 | (byte & VARUINT_BYTE)
        if byte & VARUINT_HAS_NEXT == 0:
            return result

        byte = self.readBits(8) # byte 4
        result = result << 7 | (byte & VARUINT_BYTE)
        if byte & VARUINT_HAS_NEXT == 0:
            return result

        byte = self.readBits(8) # byte 5
        result = result << 7 | (byte & VARUINT_BYTE)
        if byte & VARUINT_HAS_NEXT == 0:
            return result

        byte = self.readBits(8) # byte 6
        result = result << 7 | (byte & VARUINT_BYTE)
        if byte & VARUINT_HAS_NEXT == 0:
            return result

        byte = self.readBits(8) # byte 7
        result = result << 7 | (byte & VARUINT_BYTE)
        if byte & VARUINT_HAS_NEXT == 0:
            return result

        byte = self.readBits(8) # byte 8
        result = result << 7 | (byte & VARUINT_BYTE)
        if byte & VARUINT_HAS_NEXT == 0:
            return result

        result = result << 8 | self.readBits(8) # byte 9
        return result

    def readVarSize(self) -> int:
        """
        Reads variable size integer value from the bit stream.

        :returns: Variable size integer value.
        :raises PythonRuntimeException: If read variable size integer is out of range.
        """

        byte = self.readBits(8) # byte 1
        result = byte & VARUINT_BYTE
        if byte & VARUINT_HAS_NEXT == 0:
            return result

        byte = self.readBits(8) # byte 2
        result = result << 7 | (byte & VARUINT_BYTE)
        if byte & VARUINT_HAS_NEXT == 0:
            return result

        byte = self.readBits(8) # byte 3
        result = result << 7 | (byte & VARUINT_BYTE)
        if byte & VARUINT_HAS_NEXT == 0:
            return result

        byte = self.readBits(8) # byte 4
        result = result << 7 | (byte & VARUINT_BYTE)
        if byte & VARUINT_HAS_NEXT == 0:
            return result

        result = result << 8 | self.readBits(8) # byte 5
        if result > VARSIZE_MAX_VALUE:
            raise PythonRuntimeException("BitStreamReader: Read value '%d' is out of range for varsize type!" %
                                         result)

        return result

    def readFloat16(self) -> float:
        """
        Read 16-bits from the stream as a float value encoded according to IEEE 754 binary16.

        :returns: Read float value.
        :raises PythonRuntimeException: If the reading goes behind the stream.
        """

        return convertUInt16ToFloat(self.readBits(16))

    def readFloat32(self) -> float:
        """
        Read 32-bits from the stream as a float value encoded according to IEEE 754 binary32.

        :returns: Read float value.
        :raises PythonRuntimeException: If the reading goes behind the stream.
        """

        return convertUInt32ToFloat(self.readBits(32))

    def readFloat64(self) -> float:
        """
        Read 64-bits from the stream as a float value encoded according to IEEE 754 binary64.

        :returns: Read float value.
        :raises PythonRuntimeException: If the reading goes behind the stream.
        """

        return convertUInt64ToFloat(self.readBits(64))

    def readString(self) -> str:
        """
        Reads string from the stream.

        :returns: Read string.
        :raises PythonRuntimeException: If the reading goes behind the stream.
        """

        length = self.readVarSize()
        value = bytearray()
        for _ in range(length):
            value.append(self.readBits(8))

        return value.decode("utf-8")

    def readBool(self) -> bool:
        """
        Reads single bit as a bool value.

        :returns: Read bool values.
        :raises PythonRuntimeException: If the reading goes behind the stream.
        """

        return self.readBits(1) != 0

    def readBitBuffer(self) -> BitBuffer:
        """
        Reads a bit buffer from the stream.

        :returns: Read bit buffer.
        :raises PythonRuntimeException: If the reading goes behind the stream.
        """

        bitSize = self.readVarSize()
        numBytesToRead = bitSize // 8
        numRestBits = bitSize - numBytesToRead * 8
        byteSize = (bitSize + 7) // 8
        readBuffer = bytearray(byteSize)
        beginBitPosition = self._bitPosition
        if (beginBitPosition & 0x07) != 0:
            # we are not aligned to byte
            for i in range(numBytesToRead):
                readBuffer[i] = self.readBits(8)
        else:
            # we are aligned to byte
            self.setBitPosition(beginBitPosition + numBytesToRead * 8)
            beginBytePosition = beginBitPosition // 8
            buffer = self._bitBuffer.getBuffer()
            readBuffer[0:numBytesToRead] = buffer[beginBytePosition:beginBytePosition + numBytesToRead]

        if numRestBits != 0:
            readBuffer[numBytesToRead] = self.readBits(numRestBits) << (8 - numRestBits)

        return BitBuffer(readBuffer, bitSize)

    def getBitPosition(self) -> int:
        """
        Gets current bit position.

        :returns: Current bit position.
        """

        return self._bitPosition

    def setBitPosition(self, bitPosition: int) -> None:
        """
        Sets bit position.

        :param bitPosition: New bit position.
        :raises PythonRuntimeException: If the position is not within the stream.
        """

        if bitPosition < 0:
            raise PythonRuntimeException("BitStreamReader: Cannot set negative bit position!")
        if bitPosition > self._bitBuffer.getBitSize():
            raise PythonRuntimeException("BitStreamReader: Setting bit position behind the stream!")

        self._bitPosition = bitPosition

    def alignTo(self, alignment: int) -> None:
        """
        Aligns the bit position according to the aligning value.

        :param alignment: An aligning value to use.
        :raises PythonRuntimeException: If the aligning moves behind the stream."
        """

        offset = self._bitPosition % alignment
        if offset != 0:
            self.setBitPosition(self._bitPosition + alignment - offset)

    def getBufferBitSize(self) -> int:
        """
        Gets size of the underlying buffer in bits.

        :returns: Buffer bit size.
        """

        return self._bitBuffer.getBitSize()

VARINT_SIGN_1 = 0x80
VARINT_BYTE_1 = 0x3f
VARINT_BYTE_N = 0x7f
VARINT_HAS_NEXT_1 = 0x40
VARINT_HAS_NEXT_N = 0x80
VARUINT_BYTE = 0x7f
VARUINT_HAS_NEXT = 0x80
VARSIZE_MAX_VALUE = (1 << 31) - 1
