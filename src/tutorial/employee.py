# Automatically generated by Zserio Python generator version 1.0.0 using Zserio core 2.13.0.
# Generator setup: writerCode, pubsubCode, serviceCode, sqlCode

from __future__ import annotations

import typing
import zserio

import tutorial.experience
import tutorial.role

class Employee:
    def __init__(
            self,
            age_: int = int(),
            name_: str = str(),
            salary_: int = int(),
            bonus_: typing.Optional[int] = None,
            role_: typing.Union[tutorial.role.Role, None] = None,
            skills_: typing.Optional[typing.List[tutorial.experience.Experience]] = None) -> None:
        self._age_ = age_
        self._name_ = name_
        self._salary_ = salary_
        self._bonus_ = bonus_
        self._role_ = role_
        if skills_ is None:
            self._skills_ = None
        else:
            self._skills_ = zserio.array.Array(zserio.array.ObjectArrayTraits(self._ZserioElementFactory_skills()), skills_, is_auto=True)

    @classmethod
    def from_reader(
            cls: typing.Type['Employee'],
            zserio_reader: zserio.BitStreamReader) -> 'Employee':
        self = object.__new__(cls)

        self.read(zserio_reader)

        return self

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Employee):
            return ((self._age_ == other._age_) and
                    (self._name_ == other._name_) and
                    (self._salary_ == other._salary_) and
                    (not other.is_bonus_used() if not self.is_bonus_used() else (self._bonus_ == other._bonus_)) and
                    (self._role_ == other._role_) and
                    (not other.is_skills_used() if not self.is_skills_used() else (self._skills_ == other._skills_)))

        return False

    def __hash__(self) -> int:
        result = zserio.hashcode.HASH_SEED
        result = zserio.hashcode.calc_hashcode_int32(result, self._age_)
        result = zserio.hashcode.calc_hashcode_string(result, self._name_)
        result = zserio.hashcode.calc_hashcode_int32(result, self._salary_)
        if self.is_bonus_used():
            result = zserio.hashcode.calc_hashcode_int32(result, self._bonus_)
        result = zserio.hashcode.calc_hashcode_object(result, self._role_)
        if self.is_skills_used():
            result = zserio.hashcode.calc_hashcode_object(result, self._skills_)

        return result

    @property
    def age(self) -> int:
        return self._age_

    @age.setter
    def age(self, age_: int) -> None:
        self._age_ = age_

    @property
    def name(self) -> str:
        return self._name_

    @name.setter
    def name(self, name_: str) -> None:
        self._name_ = name_

    @property
    def salary(self) -> int:
        return self._salary_

    @salary.setter
    def salary(self, salary_: int) -> None:
        self._salary_ = salary_

    @property
    def bonus(self) -> typing.Optional[int]:
        return self._bonus_

    @bonus.setter
    def bonus(self, bonus_: typing.Optional[int]) -> None:
        self._bonus_ = bonus_

    def is_bonus_used(self) -> bool:
        return self.is_bonus_set()

    def is_bonus_set(self) -> bool:
        return not self._bonus_ is None

    def reset_bonus(self) -> None:
        self._bonus_ = None

    @property
    def role(self) -> typing.Union[tutorial.role.Role, None]:
        return self._role_

    @role.setter
    def role(self, role_: typing.Union[tutorial.role.Role, None]) -> None:
        self._role_ = role_

    @property
    def skills(self) -> typing.Optional[typing.List[tutorial.experience.Experience]]:
        return None if self._skills_ is None else self._skills_.raw_array

    @skills.setter
    def skills(self, skills_: typing.Optional[typing.List[tutorial.experience.Experience]]) -> None:
        if skills_ is None:
            self._skills_ = None
        else:
            self._skills_ = zserio.array.Array(zserio.array.ObjectArrayTraits(self._ZserioElementFactory_skills()), skills_, is_auto=True)

    def is_skills_used(self) -> bool:
        return self._role_ == tutorial.role.Role.DEVELOPER

    def is_skills_set(self) -> bool:
        return not self._skills_ is None

    def reset_skills(self) -> None:
        self._skills_ = None

    def bitsizeof(self, bitposition: int = 0) -> int:
        end_bitposition = bitposition
        end_bitposition += 8
        end_bitposition += zserio.bitsizeof.bitsizeof_string(self._name_)
        end_bitposition += 16
        end_bitposition += 1
        if self.is_bonus_used():
            end_bitposition += 16
        end_bitposition += self._role_.bitsizeof(end_bitposition)
        if self.is_skills_used():
            end_bitposition += self._skills_.bitsizeof(end_bitposition)

        return end_bitposition - bitposition

    def initialize_offsets(self, bitposition: int = 0) -> int:
        end_bitposition = bitposition
        end_bitposition += 8
        end_bitposition += zserio.bitsizeof.bitsizeof_string(self._name_)
        end_bitposition += 16
        end_bitposition += 1
        if self.is_bonus_used():
            end_bitposition += 16
        end_bitposition = self._role_.initialize_offsets(end_bitposition)
        if self.is_skills_used():
            end_bitposition = self._skills_.initialize_offsets(end_bitposition)

        return end_bitposition

    def read(self, zserio_reader: zserio.BitStreamReader) -> None:
        self._age_ = zserio_reader.read_bits(8)
        # check constraint
        if not (self._age_ <= 65):
            raise zserio.PythonRuntimeException("Constraint violated for field Employee.age!")

        self._name_ = zserio_reader.read_string()

        self._salary_ = zserio_reader.read_bits(16)

        if zserio_reader.read_bool():
            self._bonus_ = zserio_reader.read_bits(16)
        else:
            self._bonus_ = None

        self._role_ = tutorial.role.Role.from_reader(zserio_reader)

        if self.is_skills_used():
            self._skills_ = zserio.array.Array.from_reader(zserio.array.ObjectArrayTraits(self._ZserioElementFactory_skills()), zserio_reader, is_auto=True)
        else:
            self._skills_ = None

    def write(self, zserio_writer: zserio.BitStreamWriter) -> None:
        # check constraint
        if not (self._age_ <= 65):
            raise zserio.PythonRuntimeException("Constraint violated for field Employee.age!")
        zserio_writer.write_bits(self._age_, 8)

        zserio_writer.write_string(self._name_)

        zserio_writer.write_bits(self._salary_, 16)

        if self.is_bonus_used():
            zserio_writer.write_bool(True)
            zserio_writer.write_bits(self._bonus_, 16)
        else:
            zserio_writer.write_bool(False)

        self._role_.write(zserio_writer)

        if self.is_skills_used():
            self._skills_.write(zserio_writer)

    class _ZserioElementFactory_skills:
        IS_OBJECT_PACKABLE = False

        @staticmethod
        def create(zserio_reader: zserio.BitStreamReader, zserio_index: int) -> tutorial.experience.Experience:
            del zserio_index
            return tutorial.experience.Experience.from_reader(zserio_reader)
