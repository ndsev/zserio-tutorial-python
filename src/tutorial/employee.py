"""
Automatically generated by Zserio Python extension version 2.4.0.
Generator setup: writerCode, pubsubCode, serviceCode, sqlCode.
"""

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
            self._skills_ = zserio.array.Array(zserio.array.ObjectArrayTraits(self._element_creator_skills, self._packed_element_creator_skills, tutorial.experience.Experience.create_packing_context), skills_, is_auto=True)

    @classmethod
    def from_reader(
            cls: typing.Type['Employee'],
            zserio_reader: zserio.BitStreamReader) -> 'Employee':
        instance = cls()
        instance.read(zserio_reader)

        return instance

    @classmethod
    def from_reader_packed(
            cls: typing.Type['Employee'],
            zserio_context_node: zserio.array.PackingContextNode,
            zserio_reader: zserio.BitStreamReader) -> 'Employee':
        instance = cls()
        instance.read_packed(zserio_context_node, zserio_reader)

        return instance

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Employee):
            return (self._age_ == other._age_ and
                    self._name_ == other._name_ and
                    self._salary_ == other._salary_ and
                    (not self.is_bonus_used() or self._bonus_ == other._bonus_) and
                    self._role_ == other._role_ and
                    (not self.is_skills_used() or self._skills_ == other._skills_))

        return False

    def __hash__(self) -> int:
        result = zserio.hashcode.HASH_SEED
        result = zserio.hashcode.calc_hashcode(result, hash(self._age_))
        result = zserio.hashcode.calc_hashcode(result, hash(self._name_))
        result = zserio.hashcode.calc_hashcode(result, hash(self._salary_))
        if self.is_bonus_used():
            result = zserio.hashcode.calc_hashcode(result, hash(self._bonus_))
        result = zserio.hashcode.calc_hashcode(result, hash(self._role_))
        if self.is_skills_used():
            result = zserio.hashcode.calc_hashcode(result, hash(self._skills_))

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
        return not self._bonus_ is None

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
            self._skills_ = zserio.array.Array(zserio.array.ObjectArrayTraits(self._element_creator_skills, self._packed_element_creator_skills, tutorial.experience.Experience.create_packing_context), skills_, is_auto=True)

    def is_skills_used(self) -> bool:
        return self.role == tutorial.role.Role.DEVELOPER

    @staticmethod
    def create_packing_context(context_node: zserio.array.PackingContextNode) -> None:
        context_node.create_child().create_context()
        context_node.create_child()
        context_node.create_child().create_context()
        context_node.create_child().create_context()
        tutorial.role.Role.create_packing_context(context_node.create_child())
        context_node.create_child()

    def init_packing_context(self, context_node: zserio.array.PackingContextNode) -> None:
        zserio_ctx_node_age = context_node.children[0]
        zserio_ctx_node_age.context.init(self._age_)
        zserio_ctx_node_salary = context_node.children[2]
        zserio_ctx_node_salary.context.init(self._salary_)
        zserio_ctx_node_bonus = context_node.children[3]
        if self.is_bonus_used():
            zserio_ctx_node_bonus.context.init(self._bonus_)
        zserio_ctx_node_role = context_node.children[4]
        self._role_.init_packing_context(zserio_ctx_node_role)

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

    def bitsizeof_packed(self, context_node: zserio.array.PackingContextNode,
                         bitposition: int = 0) -> int:
        end_bitposition = bitposition
        zserio_ctx_node_age = context_node.children[0]
        end_bitposition += zserio_ctx_node_age.context.bitsizeof(zserio.array.BitFieldArrayTraits(8), end_bitposition, self._age_)
        end_bitposition += zserio.bitsizeof.bitsizeof_string(self._name_)
        zserio_ctx_node_salary = context_node.children[2]
        end_bitposition += zserio_ctx_node_salary.context.bitsizeof(zserio.array.BitFieldArrayTraits(16), end_bitposition, self._salary_)
        zserio_ctx_node_bonus = context_node.children[3]
        end_bitposition += 1
        if self.is_bonus_used():
            end_bitposition += zserio_ctx_node_bonus.context.bitsizeof(zserio.array.BitFieldArrayTraits(16), end_bitposition, self._bonus_)
        zserio_ctx_node_role = context_node.children[4]
        end_bitposition += self._role_.bitsizeof_packed(zserio_ctx_node_role, end_bitposition)
        if self.is_skills_used():
            end_bitposition += self._skills_.bitsizeof_packed(end_bitposition)

        return end_bitposition - bitposition

    def initialize_offsets(self, bitposition: int) -> int:
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

    def initialize_offsets_packed(self, context_node: zserio.array.PackingContextNode,
                                  bitposition: int) -> int:
        end_bitposition = bitposition
        zserio_ctx_node_age = context_node.children[0]
        end_bitposition += zserio_ctx_node_age.context.bitsizeof(zserio.array.BitFieldArrayTraits(8), end_bitposition, self._age_)
        end_bitposition += zserio.bitsizeof.bitsizeof_string(self._name_)
        zserio_ctx_node_salary = context_node.children[2]
        end_bitposition += zserio_ctx_node_salary.context.bitsizeof(zserio.array.BitFieldArrayTraits(16), end_bitposition, self._salary_)
        zserio_ctx_node_bonus = context_node.children[3]
        end_bitposition += 1
        if self.is_bonus_used():
            end_bitposition += zserio_ctx_node_bonus.context.bitsizeof(zserio.array.BitFieldArrayTraits(16), end_bitposition, self._bonus_)
        zserio_ctx_node_role = context_node.children[4]
        end_bitposition = self._role_.initialize_offsets_packed(zserio_ctx_node_role, end_bitposition)
        if self.is_skills_used():
            end_bitposition = self._skills_.initialize_offsets_packed(end_bitposition)

        return end_bitposition

    def read(self, zserio_reader: zserio.BitStreamReader) -> None:
        self._age_ = zserio_reader.read_bits(8)
        # check constraint
        if not (self.age <= 65):
            raise zserio.PythonRuntimeException("Constraint violated for field Employee.age!")

        self._name_ = zserio_reader.read_string()

        self._salary_ = zserio_reader.read_bits(16)

        if zserio_reader.read_bool():
            self._bonus_ = zserio_reader.read_bits(16)

        self._role_ = tutorial.role.Role.from_reader(zserio_reader)

        if self.is_skills_used():
            self._skills_ = zserio.array.Array.from_reader(zserio.array.ObjectArrayTraits(self._element_creator_skills, self._packed_element_creator_skills, tutorial.experience.Experience.create_packing_context), zserio_reader, is_auto=True)

    def read_packed(self, zserio_context_node: zserio.array.PackingContextNode,
                    zserio_reader: zserio.BitStreamReader) -> None:
        zserio_ctx_node_age = zserio_context_node.children[0]
        self._age_ = zserio_ctx_node_age.context.read(zserio.array.BitFieldArrayTraits(8), zserio_reader)
        # check constraint
        if not (self.age <= 65):
            raise zserio.PythonRuntimeException("Constraint violated for field Employee.age!")

        self._name_ = zserio_reader.read_string()

        zserio_ctx_node_salary = zserio_context_node.children[2]
        self._salary_ = zserio_ctx_node_salary.context.read(zserio.array.BitFieldArrayTraits(16), zserio_reader)

        zserio_ctx_node_bonus = zserio_context_node.children[3]
        if zserio_reader.read_bool():
            self._bonus_ = zserio_ctx_node_bonus.context.read(zserio.array.BitFieldArrayTraits(16), zserio_reader)

        zserio_ctx_node_role = zserio_context_node.children[4]
        self._role_ = tutorial.role.Role.from_reader_packed(zserio_ctx_node_role, zserio_reader)

        if self.is_skills_used():
            self._skills_ = zserio.array.Array.from_reader_packed(zserio.array.ObjectArrayTraits(self._element_creator_skills, self._packed_element_creator_skills, tutorial.experience.Experience.create_packing_context), zserio_reader, is_auto=True)

    def write(self, zserio_writer: zserio.BitStreamWriter, *,
              zserio_call_initialize_offsets: bool = True) -> None:
        del zserio_call_initialize_offsets

        # check constraint
        if not (self.age <= 65):
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

    def write_packed(self, zserio_context_node: zserio.array.PackingContextNode,
                     zserio_writer: zserio.BitStreamWriter) -> None:
        zserio_ctx_node_age = zserio_context_node.children[0]
        # check constraint
        if not (self.age <= 65):
            raise zserio.PythonRuntimeException("Constraint violated for field Employee.age!")
        zserio_ctx_node_age.context.write(zserio.array.BitFieldArrayTraits(8), zserio_writer, self._age_)

        zserio_writer.write_string(self._name_)

        zserio_ctx_node_salary = zserio_context_node.children[2]
        zserio_ctx_node_salary.context.write(zserio.array.BitFieldArrayTraits(16), zserio_writer, self._salary_)

        zserio_ctx_node_bonus = zserio_context_node.children[3]
        if self.is_bonus_used():
            zserio_writer.write_bool(True)
            zserio_ctx_node_bonus.context.write(zserio.array.BitFieldArrayTraits(16), zserio_writer, self._bonus_)
        else:
            zserio_writer.write_bool(False)

        zserio_ctx_node_role = zserio_context_node.children[4]
        self._role_.write_packed(zserio_ctx_node_role, zserio_writer)

        if self.is_skills_used():
            self._skills_.write_packed(zserio_writer)

    def _element_creator_skills(self, zserio_reader: zserio.BitStreamReader, zserio_index: int) -> tutorial.experience.Experience:
        del zserio_index
        return tutorial.experience.Experience.from_reader(zserio_reader)

    def _packed_element_creator_skills(
            self, zserio_context_node: zserio.array.PackingContextNode,
            zserio_reader: zserio.BitStreamReader, zserio_index: int) -> tutorial.experience.Experience:
        del zserio_index
        return tutorial.experience.Experience.from_reader_packed(zserio_context_node, zserio_reader)