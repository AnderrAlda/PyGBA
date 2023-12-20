import dis

def add(a, b):
    return a + b

def getInstructions (add):
    # Get the instruction objects using dis.get_instructions
    instructions = dis.get_instructions(add)

    # Print each instruction object in a formatted way
    for instruction in instructions:
        # Extract the relevant information from the instruction object
        opcode = instruction.opname
        arg = instruction.argval
        offset = instruction.offset

        # Print the information in a formatted way, handling the case where arg is None
        print(f"{offset:04x}: {opcode:<10}  {arg if arg is not None else '':<5}")


def main():
    
    print("this function disassembles the object into its constituent instructions:")
    dis.dis(add)   
    print()

    print("get_instructions function shows the opcode:")
    getInstructions(add)
    print()

    print("the byte-compiled code of our function:")
    print(add.__code__.co_code)

if __name__ == '__main__':
    main()
