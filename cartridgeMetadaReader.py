import struct
from collections import namedtuple
from pathlib import Path

FIELDS = [
    (None, "="),
    (None, 'xxxx'),
    (None, '48x'),
    ("title", '15s'),
    ("cgb", 'B'),
    ("new_licensee_code", 'H'),
    ("sgb", 'B'),
    ("cartridge_type", 'B'),
    ("rom_size", 'B'),
    ("ram_size", 'B'),
    ("destination_code", 'B'),
    ("old_licensee_code", 'B'),
    ("mask_rom_version", 'B'),
    ("header_checksum", 'B'),
    ("global_checksum", 'H'),
]

CARTRIDGE_HEADER = "".join(format_type for _, format_type in FIELDS)

CartridgeMetadata = namedtuple(
    "CartridgeMetadata",
    [field_name for field_name, _ in FIELDS if field_name is not None],
)

def read_cartridge_metadata(buffer, offset: int = 0x100):
    data = struct.unpack_from(CARTRIDGE_HEADER, buffer, offset=offset)
    return CartridgeMetadata._make(data)

def print_cartridge_metadata(metadata):
    print("Cartridge Metadata:")
    for field, value in metadata._asdict().items():
        if field == "title":
            value = value.decode("utf-8").rstrip("\x00")  
        print(f"{field}={repr(value)}")

def main():
    p = Path('snake.gb')      
    metadata = read_cartridge_metadata(p.read_bytes())
    print_cartridge_metadata(metadata)

if __name__ == "__main__":
    main()

