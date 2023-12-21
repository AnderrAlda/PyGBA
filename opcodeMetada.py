import json
import struct
from dataclasses import dataclass
from typing import Literal
from collections import namedtuple

@dataclass(frozen=True)
class Operand:
    immediate: bool
    name: str
    bytes: int
    value: int | None
    adjust: Literal["+", "-"] | None

@dataclass
class Instruction:
    opcode: int
    immediate: bool
    operands: list[Operand]
    cycles: list[int]
    bytes: int
    mnemonic: str
    comment: str = ""

def generate_human_readable(instruction: Instruction):
    opcode = instruction.opcode
    mnemonic = instruction.mnemonic
    operands = ', '.join([operand.name for operand in instruction.operands])

    # Print details along with values
    print(f"Opcode: {opcode}")
    print(f"Mnemonic: {mnemonic}")
    if operands:
        print(f"Operands: {operands}")
    print()  # Add an empty line for clarity between opcodes

# Cartridge Metadata Fields
FIELDS = [
    (None, "="),  # "Native" endian.
    # ... (other fields as described in the explanation)
]

# Constants for Cartridge Header
HEADER_START = 0x100
HEADER_END = 0x14F
HEADER_SIZE = (HEADER_END - HEADER_START) + 1

# Cartridge Header Format String
CARTRIDGE_HEADER = "".join(format_type for _, format_type in FIELDS)

# Cartridge Metadata namedtuple
CartridgeMetadata = namedtuple(
    "CartridgeMetadata",
    [field_name for field_name, _ in FIELDS if field_name is not None],
)


def read_cartridge_metadata(buffer, offset: int = 0x100):
    """
    Unpacks the cartridge metadata from `buffer` at `offset` and
    returns a `CartridgeMetadata` object.
    """
    data = struct.unpack_from(CARTRIDGE_HEADER, buffer, offset=offset)
    return CartridgeMetadata._make(data)


def main():
    # Load the opcode data from the JSON file (from the emulator)
    with open('Opcodes.json', 'r') as file:
        opcode_data = json.load(file)

    # Prompt user for cartridge metadata file
    cartridge_file = input("Enter the cartridge file path: ").strip()

    # Read cartridge metadata
    try:
        with open(cartridge_file, 'rb') as f:
            cartridge_data = f.read()
            metadata = read_cartridge_metadata(cartridge_data)

            # Display cartridge metadata
            print("Cartridge Metadata:")
            for field_name, value in zip(metadata._fields, metadata):
                print(f"{field_name}: {value}")

            # Display human-readable details for the selected opcode (from the emulator)
            # ... (call to generate_human_readable or other relevant display)
    except FileNotFoundError:
        print("File not found. Please provide a valid file path.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

