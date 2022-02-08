"""TODO: Fill info."""
from typing import List, Tuple

import numpy as np
import pickle
from decompr import img_parser, constants


class LZWStrategy:
    
    @staticmethod
    def compress(uncompressed: str) -> list:
        """Compresses a string to a list of output symbols."""
        # Build the dictionary.
        dict_size = 256
        dictionary = { chr(i): chr(i) for i in range(dict_size) }

        w = ""
        result = []
        for c in uncompressed:
            wc = w + c
            if wc in dictionary:
                w = wc
            else:
                result.append(dictionary[w])
                # Add wc to the dictionary
                dictionary[wc] = dict_size
                dict_size += 1
                w = c

        # Output the code for w
        if w:
            result.append(dictionary[w])
        return result


    @staticmethod
    def decompress(compressed: list) -> str:
        """Decompresses a list of output ks to a string."""
        # Build the dictionary
        dict_size = 256
        dictionary = { chr(i): chr(i) for i in range(dict_size) }

        w = result = compressed.pop(0)
        for k in compressed:
            if k in dictionary:
                entry = dictionary[k]
            elif k == dict_size:
                entry = w + w[0]
            else:
                raise ValueError('Bad compressed k: %s' % k)
            result += entry

            # Add w+entry[0] to the dictionary
            dictionary[dict_size] = w + entry[0]
            dict_size += 1

            w = entry
        return result
    

    @staticmethod
    def ascii_encode(values: np.ndarray) -> str:
        ascii_values = [ chr(value) for value in values ]
        return "".join(ascii_values)
    
    @staticmethod
    def ascii_decode(characters: str) -> list:
        int_values = [ ord(character) for character in characters ]
        return np.array(int_values)


    @staticmethod
    def bytes_encode(entries: list) -> bytes:
        bytes_list = list()
        for entry in entries:
            if type(entry) == str:
                bytes_list.append(entry.encode('utf_8'))
            if type(entry) == int:
                bytes_list.append(entry.to_bytes(4, byteorder='big'))
        return bytes_list


    @classmethod
    def compress_file(cls, img_path: str) -> None:
        """"""
        pixels_dec = img_parser.get_pixels_declist(img_path)

        img_h = img_parser.bytes_to_integer(
            img_parser.read_file_slice(
                img_fpath=img_path,
                indexes=constants.IMAGE_HEIGHT), sign=True
        )
        img_w = img_parser.bytes_to_integer(
            img_parser.read_file_slice(
                img_fpath=img_path,
                indexes=constants.IMAGE_WIDTH), sign=True
        )

        b_channel, g_channel, r_channel = img_parser.parse_channels(
            pixels_dec
        )

        data_b = cls.ascii_encode(b_channel)
        compressed_b = cls.compress(data_b)

        data_g = cls.ascii_encode(g_channel)
        compressed_g = cls.compress(data_g)

        data_r = cls.ascii_encode(r_channel)
        compressed_r = cls.compress(data_r)

        compressed_channels = {
            42: compressed_b, # b channel
            71: compressed_g, # g channel
            82: compressed_r,  # r channel
            100: {
                104: img_h,
                119: img_w
            }
        }

        raw_data = pickle.dumps(compressed_channels)

        with open(f"{img_path[:-4]}.lzw", 'wb') as img_comp:
            img_comp.write(raw_data)


    @classmethod
    def decompress_file(cls, c_img_path: str) -> None:
        """"""
        with open(c_img_path, 'rb') as c_imgfile:
            c_img_file_bytes = c_imgfile.read()
        
        compressed_channels = pickle.loads(c_img_file_bytes)

        compressed_b = compressed_channels[42]
        compressed_g = compressed_channels[71]
        compressed_r = compressed_channels[82]

        img_h, img_w = compressed_channels[100][104], compressed_channels[100][119]

        b_channel = cls.ascii_decode(cls.decompress(compressed_b))
        g_channel = cls.ascii_decode(cls.decompress(compressed_g))
        r_channel = cls.ascii_decode(cls.decompress(compressed_r))

        b_channel = [int(value) for value in b_channel]
        g_channel = [int(value) for value in g_channel]
        r_channel = [int(value) for value in r_channel]

        bgr_values = [
            [vb, vg, vr]
            for vb, vg, vr in zip(b_channel, g_channel, r_channel)
        ]

        bgr_values_bytes = img_parser.convert_pixels_to_bytes(bgr_values)

        print(type(bgr_values_bytes))

        # print(img_h)
        # print(img_w)

        with open('image_processor/decompr/bmp_header.txt', 'r') as header_txt:
            header_values = header_txt.read()
        
        print(hex(img_w))

        print(header_values[18:22])

        print(hex(img_h))

        print(header_values[22:26])

        with open(f"{c_img_path[:-4]}_uncompressed.bmp", 'wb') as uncomp_img:
            uncomp_img.write(bgr_values_bytes)
