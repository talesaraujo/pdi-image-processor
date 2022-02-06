"""TODO: Fill in this with useful info"""
from typing import Tuple, List
import os
from image_processor.decompr import constants


def bytes_to_integer(bytes_sequence: bytes, sign: bool=False) -> int:
    """Given a sequence of bytes, it returns the integer representation of
    such sequence, ordered via little endian setup."""
    return int.from_bytes(bytes_sequence, byteorder="little", signed=sign)


def read_file_slice(img_fpath: str, indexes: tuple=(0, -1)) -> bytes:
    """Returns a bytes sequence indexed via byte positions."""
    start_byte, end_byte = indexes

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


def get_pixels_info(img_fpath: str) -> List[tuple]:
    """Returns only the information related to the image pixels."""
    pixel_data_offset = read_file_slice(
        img_fpath,
        indexes=constants.PIXEL_DATA_OFFSET
    )
    pixel_data_offset = bytes_to_integer(pixel_data_offset)

    file_size = os.path.getsize(img_fpath)
    bytelist = list()

    with open(img_fpath, "rb") as img_file:
        for counter in range(file_size):
            byte = img_file.read(1)
            if counter >= pixel_data_offset:
                bytelist.append(byte)
                
    return bytelist


def get_pixels_hexlist(img_fpath: str) -> list:
    """Returns a list of 3d tuples with the hexadecimal values that represent
    the BGR colors."""
    pixels_info = get_pixels_info(img_fpath)

    pixels_list = list()

    for i in range(len(pixels_info)):
        if (i % 3) == 0:
            pixels_list.append(
                (pixels_info[i], pixels_info[i+1], pixels_info[i+2])
            )
    
    pixels_list = [
        tuple(pixel[i].hex().upper() for i in range(3))
        for pixel in pixels_list
    ]

    return pixels_list


def convert_to_decimal(pixels_hexlist: list) -> list:
    """Returns the values in decimal format, as strings, for the BGR channels
    that are represented by the input of hexadecimal values."""
    pixel_list = [
        tuple(str(int(pixel[i], 16)) for i in range(3))
        for pixel in pixels_hexlist
    ]

    return pixel_list


# def parse_imgfile(filepath: str) -> Tuple[List[bytes], List[bytes], List[bytes]]:
#     """TODO: Fill in"""
#     pixel_data_offset = read_file_slice(
#         img_fpath=filepath,
#         indexes=constants.IMAGE_WIDTH
#         )
    
#     print(f"HEX {pixel_data_offset.hex()}")
#     print(f"DEC {bytes_to_integer(pixel_data_offset, sign=False)}")
