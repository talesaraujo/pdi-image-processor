"""Mapping of bitmap file (.bmp) data."""

"""
BITMAPFILEHEADER

Fields: 5
Total Size: 14 bytes
"""
# A two character string value in ASCII. It must be 'BM' or '0x42' 0x4D'
FILETYPE            = ( 0,  2)

# An (unsigned) integer representing entire file size in bytes
FILESIZE            = ( 2,  6)

# To be utilized by an image processing application. 
# Initialized to '0' (unsigned) integer value
RESERVED_1          = ( 6,  8)

# To be utilized by an image processing application. 
# Initialized to '0' (unsigned) integer value
RESERVED_2          = ( 8, 10)

# An (unsigned) integer representing the offset of actual data in bytes
# It means the number of bytes between the start of the file at 0 and the
# first byte of the pixel data
PIXEL_DATA_OFFSET   = (10, 14)

"""
BITMAPINFOHEADER

Fields: 11
Total Size: 40 bytes
"""
# An (unsigned) integer representing the header size in bytes.
# It should be '40' in decimal to represent BITMAPINFOHEADER header type.
HEADER_SIZE         = (14, 18)

# An (signed) integer representing the WIDTH of the final image in pixels
IMAGE_WIDTH         = (18, 22)

# An (signed) integer representing the HEIGHT of the final image in pixels
IMAGE_HEIGHT        = (22, 26)

# An (unsigned) integer representing the number of color planes of the target
# device. Should be '1' in decimal.
PLANES              = (26, 28)

# An (unsigned) integer representing the number of bits (memory) a pixel takes,
# in pixel data, to represent a color.
BITS_PER_PIXEL      = (28, 30)

# An (unsigned) integer representing the value of compression to use. Should be
# '0' in decimal to represent uncompressed data (identified by 'BI_RGB')
COMPRESSION         = (30, 34)

# An (unsigned) integer representing the final size of the compressed image.
# Should be '0' in decimal when no compression algorithm is used.
IMAGE_SIZE          = (34, 38)

# An (signed) integer representing the horizontal resolution of the target 
# device. This parameter will be adjusted by the image processing application
# but should be set to '0' in decimal to indicate no preference.
XPIXELS_PER_METER   = (38, 42)

# An (signed) integer representing the vertical resolution of the target 
# device. This parameter will be adjusted by the image processing application
# but should be set to '0' in decimal to indicate no preference.
YPIXELS_PER_METER   = (42, 46)

# An (unsigned) integer representing the number of colors in the color pallet
# (size of the color pallet or color table). If this is set to '0' in decimal,
# it means 2^BITS_PER_PIXEL colors are used.
TOTAL_COLORS        = (46, 50)

# An (unsigned) integer representing the number of important colors. Generally
# ignored by setting '0' decimal value.
IMPORTANT_COLORS    = (50, 54)

"""Color Table:?"""
CT_RED              = (55, 56)
CT_GREEN            = (56, 57)
CT_BLUE             = (57, 58)
CT_RESERVED         = (58, 59)

# Benchmark image has 284160 pixels
# Pixels starts at position 122
STARTING_BYTE       = 122 # TODO: Set this dinamically via pixel_data_offset
