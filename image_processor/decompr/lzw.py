"""TODO: Fill info."""
from typing import List, Tuple
import numpy as np


class LZWStrategy:
    
    @staticmethod
    def compress(uncompressed):
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
    def decompress(compressed):
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
    def compress_channels(cls, channels: Tuple[int]) -> dict:

        data_b = cls.ascii_encode(channels[0])
        compressed_b = cls.compress(data_b)

        data_g = cls.ascii_encode(channels[1])
        compressed_g = cls.compress(data_g)

        data_r = cls.ascii_encode(channels[2])
        compressed_r = cls.compress(data_r)

        compressed_channels = {
            42: compressed_b, # b channel
            71: compressed_g, # g channel
            82: compressed_r  # r channel
        }

        return compressed_channels
