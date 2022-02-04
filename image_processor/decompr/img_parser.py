"""TODO: Fill in this with useful info"""
from typing import Tuple, List
import os

def read_file_slice(img_fpath: str, start_byte: int=0, end_byte: int=-1) -> bytes:
    """Returns a bytes sequence indexed via byte"""
    file_size = os.path.getsize(img_fpath)

    if end_byte < 0:
        end_byte = file_size

    bytelist = list()

    with open(img_fpath, "rb") as img_file:
        for counter in range(file_size):
            byte = img_file.read(1)
            if start_byte <= counter < end_byte:
                bytelist.append(byte)

    return b"".join(bytelist)


def parse_imgfile(filepath: str) -> Tuple[List[bytes], List[bytes], List[bytes]]:
    """TODO: Fill in"""
    FILETYPE = read_file_slice(filepath, 0, 2)
    FILESIZE = read_file_slice(filepath, 2, 6)
    RESERVED = read_file_slice(filepath, 6, 10)
    PIXEL_DATA_OFFSET = read_file_slice(filepath, 10, 14)

    print(PIXEL_DATA_OFFSET)
    print(bytes_to_integer(PIXEL_DATA_OFFSET))


def bytes_to_integer(bytes_sequence: bytes) -> int:
    return int.from_bytes(bytes_sequence, byteorder="little", signed=False)



# def get_header(filepath: str) -> bytes:
#     with open(filepath, "rb") as img_file:
#         h_bytes = img_file.read(14)
#     return h_bytes
