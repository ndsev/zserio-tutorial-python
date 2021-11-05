"""
Automatically generated by Zserio Python extension version 2.4.2.
Generator setup: writerCode, pubsubCode, serviceCode, sqlCode.
"""

from __future__ import annotations

import typing
import zserio

import tutorial.language

class Experience:
    def __init__(
            self,
            years_of_experience_: int = int(),
            programming_language_: typing.Union[tutorial.language.Language, None] = None) -> None:
        self._years_of_experience_ = years_of_experience_
        self._programming_language_ = programming_language_

    @classmethod
    def from_reader(
            cls: typing.Type['Experience'],
            zserio_reader: zserio.BitStreamReader) -> 'Experience':
        instance = cls()
        instance.read(zserio_reader)

        return instance

    @classmethod
    def from_reader_packed(
            cls: typing.Type['Experience'],
            zserio_context_node: zserio.array.PackingContextNode,
            zserio_reader: zserio.BitStreamReader) -> 'Experience':
        instance = cls()
        instance.read_packed(zserio_context_node, zserio_reader)

        return instance

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Experience):
            return (self._years_of_experience_ == other._years_of_experience_ and
                    self._programming_language_ == other._programming_language_)

        return False

    def __hash__(self) -> int:
        result = zserio.hashcode.HASH_SEED
        result = zserio.hashcode.calc_hashcode(result, hash(self._years_of_experience_))
        result = zserio.hashcode.calc_hashcode(result, hash(self._programming_language_))

        return result

    @property
    def years_of_experience(self) -> int:
        return self._years_of_experience_

    @years_of_experience.setter
    def years_of_experience(self, years_of_experience_: int) -> None:
        self._years_of_experience_ = years_of_experience_

    @property
    def programming_language(self) -> typing.Union[tutorial.language.Language, None]:
        return self._programming_language_

    @programming_language.setter
    def programming_language(self, programming_language_: typing.Union[tutorial.language.Language, None]) -> None:
        self._programming_language_ = programming_language_

    @staticmethod
    def create_packing_context(zserio_context_node: zserio.array.PackingContextNode) -> None:
        zserio_context_node.create_child().create_context()
        tutorial.language.Language.create_packing_context(zserio_context_node.create_child())

    def init_packing_context(self, zserio_context_node: zserio.array.PackingContextNode) -> None:
        zserio_context_node.children[0].context.init(zserio.array.BitFieldArrayTraits(6), self._years_of_experience_)
        self._programming_language_.init_packing_context(zserio_context_node.children[1])

    def bitsizeof(self, bitposition: int = 0) -> int:
        end_bitposition = bitposition
        end_bitposition += 6
        end_bitposition += self._programming_language_.bitsizeof(end_bitposition)

        return end_bitposition - bitposition

    def bitsizeof_packed(self, zserio_context_node: zserio.array.PackingContextNode,
                         bitposition: int = 0) -> int:
        end_bitposition = bitposition
        end_bitposition += zserio_context_node.children[0].context.bitsizeof(zserio.array.BitFieldArrayTraits(6), self._years_of_experience_)
        end_bitposition += self._programming_language_.bitsizeof_packed(zserio_context_node.children[1], end_bitposition)

        return end_bitposition - bitposition

    def initialize_offsets(self, bitposition: int) -> int:
        end_bitposition = bitposition
        end_bitposition += 6
        end_bitposition = self._programming_language_.initialize_offsets(end_bitposition)

        return end_bitposition

    def initialize_offsets_packed(self, zserio_context_node: zserio.array.PackingContextNode,
                                  bitposition: int) -> int:
        end_bitposition = bitposition
        end_bitposition += zserio_context_node.children[0].context.bitsizeof(zserio.array.BitFieldArrayTraits(6), self._years_of_experience_)
        end_bitposition = self._programming_language_.initialize_offsets_packed(zserio_context_node.children[1], end_bitposition)

        return end_bitposition

    def read(self, zserio_reader: zserio.BitStreamReader) -> None:
        self._years_of_experience_ = zserio_reader.read_bits(6)
        self._programming_language_ = tutorial.language.Language.from_reader(zserio_reader)

    def read_packed(self, zserio_context_node: zserio.array.PackingContextNode,
                    zserio_reader: zserio.BitStreamReader) -> None:
        self._years_of_experience_ = zserio_context_node.children[0].context.read(zserio.array.BitFieldArrayTraits(6), zserio_reader)

        self._programming_language_ = tutorial.language.Language.from_reader_packed(zserio_context_node.children[1], zserio_reader)

    def write(self, zserio_writer: zserio.BitStreamWriter, *,
              zserio_call_initialize_offsets: bool = True) -> None:
        del zserio_call_initialize_offsets

        zserio_writer.write_bits(self._years_of_experience_, 6)
        self._programming_language_.write(zserio_writer)

    def write_packed(self, zserio_context_node: zserio.array.PackingContextNode,
                     zserio_writer: zserio.BitStreamWriter) -> None:
        zserio_context_node.children[0].context.write(zserio.array.BitFieldArrayTraits(6), zserio_writer, self._years_of_experience_)

        self._programming_language_.write_packed(zserio_context_node.children[1], zserio_writer)
