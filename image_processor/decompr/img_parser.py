"""TODO: Fill in this with useful info"""
from typing import Tuple, List
import os

def read_file_slice(img_fpath: str, end_byte: int, start_byte: int=0) -> bytes:
    """Returns a bytes sequence indexed via byte"""
    file_size = os.path.getsize(img_fpath)

    if not end_byte:
        end_byte = file_size

    bytelist = list()

    with open(img_fpath, "rb") as img_file:
        for counter in range(file_size):
            byte = img_file.read(1)
            if start_byte <= counter < end_byte:
                bytelist.append(byte)

    return b"".join(bytelist)


def parse_imgfile(filepath: str) -> Tuple[List[bytes], List[bytes], List[bytes]]:
    with open(filepath, "rb") as img_file:
        filetype = [ img_file.read(1) for _ in range(2) ]
        filesize = [ img_file.read(1) for _ in range(4) ]
        reserved_4 = [ img_file.read(1) for _ in range(2) ]
        return filetype, filesize, reserved_4


def bytes_to_integer(bytes_sequence: bytes) -> int:
    return int.from_bytes(bytes_sequence, byteorder="little", signed=False)



# def get_header(filepath: str) -> bytes:
#     with open(filepath, "rb") as img_file:
#         h_bytes = img_file.read(14)
#     return h_bytes
