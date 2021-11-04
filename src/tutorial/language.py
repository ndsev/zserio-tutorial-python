"""
Automatically generated by Zserio Python extension version 2.4.1.
Generator setup: writerCode, pubsubCode, serviceCode, sqlCode.
"""

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
    def from_reader(cls: typing.Type['Language'], reader: zserio.BitStreamReader) -> 'Language':
        return cls(reader.read_bits(2))

    @classmethod
    def from_reader_packed(cls: typing.Type['Language'],
                           context_node: zserio.array.PackingContextNode,
                           reader: zserio.BitStreamReader) -> 'Language':
        return cls(context_node.context.read(zserio.array.BitFieldArrayTraits(2), reader))

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

    def initialize_offsets(self, bitposition: int) -> int:
        return bitposition + self.bitsizeof(bitposition)

    def initialize_offsets_packed(self, context_node: zserio.array.PackingContextNode,
                                  bitposition: int) -> int:
        return bitposition + self.bitsizeof_packed(context_node, bitposition)

    def write(self, writer: zserio.BitStreamWriter, *, zserio_call_initialize_offsets: bool = True) -> None:
        del zserio_call_initialize_offsets
        writer.write_bits(self.value, 2)

    def write_packed(self, context_node: zserio.array.PackingContextNode,
                     writer: zserio.BitStreamWriter) -> None:
        context_node.context.write(zserio.array.BitFieldArrayTraits(2), writer, self.value)
