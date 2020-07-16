"""
Automatically generated by Zserio Python extension version 2.0.0.
"""

import zserio

import tutorial.Language

class Experience():
    def __init__(self):
        self._yearsOfExperience_ = None
        self._programmingLanguage_ = None

    @classmethod
    def fromReader(cls, reader):
        instance = cls()
        instance.read(reader)

        return instance

    @classmethod
    def fromFields(cls, yearsOfExperience_, programmingLanguage_):
        instance = cls()
        instance.setYearsOfExperience(yearsOfExperience_)
        instance.setProgrammingLanguage(programmingLanguage_)

        return instance

    def __eq__(self, other):
        if isinstance(other, Experience):
            return (self._yearsOfExperience_ == other._yearsOfExperience_ and
                    self._programmingLanguage_ == other._programmingLanguage_)

        return False

    def __hash__(self):
        result = zserio.hashcode.HASH_SEED
        result = zserio.hashcode.calcHashCode(result, hash(self._yearsOfExperience_))
        result = zserio.hashcode.calcHashCode(result, hash(self._programmingLanguage_))

        return result

    def getYearsOfExperience(self):
        return self._yearsOfExperience_

    def setYearsOfExperience(self, yearsOfExperience_):
        self._yearsOfExperience_ = yearsOfExperience_

    def getProgrammingLanguage(self):
        return self._programmingLanguage_

    def setProgrammingLanguage(self, programmingLanguage_):
        self._programmingLanguage_ = programmingLanguage_

    def bitSizeOf(self, bitPosition=0):
        endBitPosition = bitPosition
        endBitPosition += 6
        endBitPosition += self._programmingLanguage_.bitSizeOf(endBitPosition)

        return endBitPosition - bitPosition

    def initializeOffsets(self, bitPosition):
        endBitPosition = bitPosition
        endBitPosition += 6
        endBitPosition += self._programmingLanguage_.bitSizeOf(endBitPosition)

        return endBitPosition

    def read(self, reader):
        self._yearsOfExperience_ = reader.readBits(6)
        self._programmingLanguage_ = tutorial.Language.Language.fromReader(reader)

    def write(self, writer, *, callInitializeOffsets=True):
        del callInitializeOffsets

        writer.writeBits(self._yearsOfExperience_, 6)
        self._programmingLanguage_.write(writer)
