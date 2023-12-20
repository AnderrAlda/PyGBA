import json
from dataclasses import dataclass
from typing import Literal

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

def main():
    # Load the opcode data from the JSON file
    with open('Opcodes.json', 'r') as file:
        opcode_data = json.load(file)

    # Prompt user to select 'unprefixed' or 'cbprefixed'
    section = input("Enter 'unprefixed' or 'cbprefixed': ").strip().lower()

    if section in opcode_data:
        # Extract selected section details
        selected_section = opcode_data[section]

        # Prompt user for opcode within the selected section
        opcode_choice = input(f"Enter the opcode within '{section}': ").strip().lower()

        if opcode_choice in selected_section:
            # Extract data for the selected opcode
            opcode_details = selected_section[opcode_choice]

            # Create Operand instances
            operands = []
            for operand_data in opcode_details['operands']:
                operand = Operand(
                    immediate=operand_data['immediate'],
                    name=operand_data['name'],
                    bytes=operand_data.get('bytes', 0),  # Set default value if 'bytes' is missing
                    value=operand_data.get('value'),
                    adjust=operand_data.get('adjust'),
                )
                operands.append(operand)

            # Create Instruction instance
            instruction = Instruction(
                opcode=int(opcode_choice, 16),  # Assuming opcodes are in hexadecimal
                immediate=opcode_details['immediate'],
                operands=operands,
                cycles=opcode_details['cycles'],
                bytes=opcode_details['bytes'],
                mnemonic=opcode_details['mnemonic'],
            )

            # Display human-readable details for the selected opcode
            generate_human_readable(instruction)
        else:
            print("Opcode not found in the selected section.")
    else:
        print("Invalid section selected. Please choose 'unprefixed' or 'cbprefixed'.")

if __name__ == "__main__":
    main()

