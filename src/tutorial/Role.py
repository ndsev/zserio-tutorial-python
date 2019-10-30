"""
Automatically generated by Zserio Python extension version 1.4.0-pre1.
"""

import enum

class Role(enum.Enum):
    DEVELOPER = 0
    TEAM_LEAD = 1
    CTO = 2

    @classmethod
    def fromReader(cls, reader):
        return cls(reader.readBits(8))

    def bitSizeOf(self, _bitPosition=0):
        return 8

    def initializeOffsets(self, bitPosition):
        return bitPosition + self.bitSizeOf(bitPosition)

    def write(self, writer):
        writer.writeBits(self.value, 8)
