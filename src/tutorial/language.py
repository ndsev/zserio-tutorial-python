# Automatically generated by Zserio Python extension version 2.11.0.
# Generator setup: writerCode, pubsubCode, serviceCode, sqlCode

from __future__ import annotations

import enum
import typing
import zserio

class Language(enum.Enum):
    CPP = 0
    JAVA = 1
    PYTHON = 2
    JS = 3

    @classmethod
    def from_name(cls: typing.Type['Language'], item_name: str) -> 'Language':
        if item_name == 'CPP':
            item = Language.CPP
        elif item_name == 'JAVA':
            item = Language.JAVA
        elif item_name == 'PYTHON':
            item = Language.PYTHON
        elif item_name == 'JS':
            item = Language.JS
        else:
            raise zserio.PythonRuntimeException(f"Enum item '{item_name}' doesn't exist in enum 'Language'!")

        return item

    @classmethod
    def from_reader(cls: typing.Type['Language'], reader: zserio.BitStreamReader) -> 'Language':
        return cls(reader.read_bits(2))

    @classmethod
    def from_reader_packed(cls: typing.Type['Language'],
                           context_node: zserio.array.PackingContextNode,
                           reader: zserio.BitStreamReader) -> 'Language':
        return cls(context_node.context.read(zserio.array.BitFieldArrayTraits(2), reader))

    def __hash__(self) -> int:
        result = zserio.hashcode.HASH_SEED
        result = zserio.hashcode.calc_hashcode_int32(result, self.value)
        return result

    @staticmethod
    def create_packing_context(context_node: zserio.array.PackingContextNode) -> None:
        context_node.create_context()

    def init_packing_context(self, context_node: zserio.array.PackingContextNode) -> None:
        context_node.context.init(zserio.array.BitFieldArrayTraits(2),
                                  self.value)

    def bitsizeof(self, _bitposition: int = 0) -> int:
        return 2

    def bitsizeof_packed(self, context_node: zserio.array.PackingContextNode,
                         _bitposition: int) -> int:
        return context_node.context.bitsizeof(zserio.array.BitFieldArrayTraits(2),
                                              self.value)

    def initialize_offsets(self, bitposition: int = 0) -> int:
        return bitposition + self.bitsizeof(bitposition)

    def initialize_offsets_packed(self, context_node: zserio.array.PackingContextNode,
                                  bitposition: int) -> int:
        return bitposition + self.bitsizeof_packed(context_node, bitposition)

    def write(self, writer: zserio.BitStreamWriter) -> None:
        writer.write_bits(self.value, 2)

    def write_packed(self, context_node: zserio.array.PackingContextNode,
                     writer: zserio.BitStreamWriter) -> None:
        context_node.context.write(zserio.array.BitFieldArrayTraits(2), writer, self.value)
