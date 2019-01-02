import zlib
import pathlib


def calculate_crc32_for_file(path: pathlib.Path) -> int:
    """Read file by path and return crc32 sum integer."""
    with open(path, 'rb') as f:
        return zlib.crc32(f.read())
