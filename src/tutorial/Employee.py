"""
Automatically generated by Zserio Python extension version 2.0.0.
"""

import zserio

import tutorial.Experience
import tutorial.Role

class Employee():
    def __init__(self):
        self._age_ = None
        self._name_ = None
        self._salary_ = None
        self._bonus_ = None
        self._role_ = None
        self._skills_ = None

    @classmethod
    def fromReader(cls, reader):
        instance = cls()
        instance.read(reader)

        return instance

    @classmethod
    def fromFields(cls, age_, name_, salary_, bonus_, role_, skills_):
        instance = cls()
        instance.setAge(age_)
        instance.setName(name_)
        instance.setSalary(salary_)
        instance.setBonus(bonus_)
        instance.setRole(role_)
        instance.setSkills(skills_)

        return instance

    def __eq__(self, other):
        if isinstance(other, Employee):
            return (self._age_ == other._age_ and
                    self._name_ == other._name_ and
                    self._salary_ == other._salary_ and
                    (not self.hasBonus() or self._bonus_ == other._bonus_) and
                    self._role_ == other._role_ and
                    (not self.hasSkills() or self._skills_ == other._skills_))

        return False

    def __hash__(self):
        result = zserio.hashcode.HASH_SEED
        result = zserio.hashcode.calcHashCode(result, hash(self._age_))
        result = zserio.hashcode.calcHashCode(result, hash(self._name_))
        result = zserio.hashcode.calcHashCode(result, hash(self._salary_))
        if self.hasBonus():
            result = zserio.hashcode.calcHashCode(result, hash(self._bonus_))
        result = zserio.hashcode.calcHashCode(result, hash(self._role_))
        if self.hasSkills():
            result = zserio.hashcode.calcHashCode(result, hash(self._skills_))

        return result

    def getAge(self):
        return self._age_

    def setAge(self, age_):
        self._age_ = age_

    def getName(self):
        return self._name_

    def setName(self, name_):
        self._name_ = name_

    def getSalary(self):
        return self._salary_

    def setSalary(self, salary_):
        self._salary_ = salary_

    def getBonus(self):
        return self._bonus_

    def setBonus(self, bonus_):
        self._bonus_ = bonus_

    def hasBonus(self):
        return not self._bonus_ is None

    def getRole(self):
        return self._role_

    def setRole(self, role_):
        self._role_ = role_

    def getSkills(self):
        return None if self._skills_ is None else self._skills_.getRawArray()

    def setSkills(self, skills_):
        self._skills_ = zserio.array.Array(zserio.array.ObjectArrayTraits(self._elementCreator_skills), skills_, isAuto=True)

    def hasSkills(self):
        return self.getRole() == tutorial.Role.Role.DEVELOPER

    def bitSizeOf(self, bitPosition=0):
        endBitPosition = bitPosition
        endBitPosition += 8
        endBitPosition += zserio.bitsizeof.getBitSizeOfString(self._name_)
        endBitPosition += 16
        endBitPosition += 1
        if self.hasBonus():
            endBitPosition += 16
        endBitPosition += self._role_.bitSizeOf(endBitPosition)
        if self.hasSkills():
            endBitPosition += self._skills_.bitSizeOf(endBitPosition)

        return endBitPosition - bitPosition

    def initializeOffsets(self, bitPosition):
        endBitPosition = bitPosition
        endBitPosition += 8
        endBitPosition += zserio.bitsizeof.getBitSizeOfString(self._name_)
        endBitPosition += 16
        endBitPosition += 1
        if self.hasBonus():
            endBitPosition += 16
        endBitPosition += self._role_.bitSizeOf(endBitPosition)
        if self.hasSkills():
            endBitPosition = self._skills_.initializeOffsets(endBitPosition)

        return endBitPosition

    def read(self, reader):
        self._age_ = reader.readBits(8)
        # check constraint
        if not (self.getAge() <= 65):
            raise zserio.PythonRuntimeException("Constraint violated for field Employee.age!")

        self._name_ = reader.readString()

        self._salary_ = reader.readBits(16)

        if reader.readBool():
            self._bonus_ = reader.readBits(16)

        self._role_ = tutorial.Role.Role.fromReader(reader)

        if self.hasSkills():
            self._skills_ = zserio.array.Array.fromReader(zserio.array.ObjectArrayTraits(self._elementCreator_skills), reader, isAuto=True)

    def write(self, writer, *, callInitializeOffsets=True):
        del callInitializeOffsets

        # check constraint
        if not (self.getAge() <= 65):
            raise zserio.PythonRuntimeException("Constraint violated for field Employee.age!")
        writer.writeBits(self._age_, 8)

        writer.writeString(self._name_)

        writer.writeBits(self._salary_, 16)

        if self.hasBonus():
            writer.writeBool(True)
            writer.writeBits(self._bonus_, 16)
        else:
            writer.writeBool(False)

        self._role_.write(writer)

        if self.hasSkills():
            self._skills_.write(writer)

    def _elementCreator_skills(self, reader, _index):
        return tutorial.Experience.Experience.fromReader(reader)
