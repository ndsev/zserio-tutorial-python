# Automatically generated by Zserio Python generator version 1.0.1 using Zserio core 2.14.0.
# Generator setup: writerCode, pubsubCode, serviceCode, sqlCode

from __future__ import annotations

import typing
import zserio

class Language(zserio.Enum):
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

    def __hash__(self) -> int:
        result = zserio.hashcode.HASH_SEED
        result = zserio.hashcode.calc_hashcode_int32(result, self.value)
        return result

    def bitsizeof(self, _bitposition: int = 0) -> int:
        return 2

    def initialize_offsets(self, bitposition: int = 0) -> int:
        return bitposition + self.bitsizeof(bitposition)

    def write(self, writer: zserio.BitStreamWriter) -> None:
        writer.write_bits(self.value, 2)
