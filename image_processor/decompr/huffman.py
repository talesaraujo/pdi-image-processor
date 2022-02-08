"""Logic related to the Huffman Coding process."""
from typing import Any, List, Tuple
from image_processor.core import sampling

import sys
import pickle
import numpy as np


class Node:
    """Provides a representation of a binary tree's node.
    
    This representation is built particularly for the Huffman Tree algorithm,
    so in addition to the child nodes, it includes the symbols and their
    probabilities in terms of frequencies. It can represent the entire tree
    as well, as long as the referred node is the root itself.
    """
    def __init__(self,
                prob: int,
                symbol: str="",
                left_child: Any=None,
                right_child: Any=None) -> None:
        self.prob = prob
        self.symbol = symbol
        self.code = ""
        self.left_child = left_child
        self.right_child = right_child
    
    def __repr__(self) -> str:
        return repr(self.__dict__)
    
    def __lt__(self, other: Any) -> bool:
        return self.prob < other.prob 


class HuffmanStrategy:

    @staticmethod
    def generate_tree(freqs: np.ndarray) -> List[Node]:
        """Generates the Huffman Tree for a certain set of symbols given their
        frequencies.  
        
        Arguments
        ---------
        freqs: numpy.ndarray
            The histogram of frequencies representing each image pixel indexed
            through the [0..255] interval

        Returns
        -------
        priority_queue: Node object
            The Node object element representing the Huffman Tree Coding
            for that set of frequencies (i.e. the root node).
        """
        # Assemble a priority queue ordered by freqs
        priority_list = np.array([(i, f) for i, f in enumerate(freqs)])
        priority_list = priority_list[np.argsort(priority_list[:, 1])]

        # At this point this list is supposed to be sorted by probability/freq
        priority_queue = [ Node(prob=fq, symbol=symb) for symb, fq in priority_list ]

        while len(priority_queue) > 1:
            # Remove the two lowest prob values
            node_0 = priority_queue.pop(0)
            node_1 = priority_queue.pop(0)

            # Create the new node
            node_0.code, node_1.code = "0", "1"
            new_node = Node(
                prob=node_0.prob + node_1.prob,
                left_child=node_0,
                right_child=node_1
            )

            # Insert the new created node
            priority_queue.append(new_node)
            # Re-sort the queue by freq/prob
            priority_queue.sort()

        # logger.debug("HUFFMAN TREE")
        # logger.debug(priority_queue[0])
        return priority_queue[0]


    @staticmethod
    def get_codes(huffman_tree: Node) -> np.ndarray:
        """Returns the symbol codes given the Huffman Tree.
        
        Performs a deep-first search with preorder approach throughout the
        Huffman Tree in order to recover all binary codes assigned to the
        symbols descripted on the leave nodes.

        Parameters
        ----------
        huffman_tree: Node
            The tree-like data structure representing the Huffman Tree Coding
            for a certain set of symbols.
        
        Returns
        -------
        encoded_strings: list of tuples
            The symbol and its binary representation according to the HT.
        t"""
        encoded_strings = list()

        def dfs_traverse(node: Node, code_string: str):
            if node is None:
                return 

            if node.code:
                code_string += node.code

            dfs_traverse(node.left_child, code_string)
            dfs_traverse(node.right_child, code_string)

            if str(node.symbol):
                encoded_strings.append(
                    [node.symbol, code_string]
                )
                code_string = code_string[:-1]
        
        dfs_traverse(huffman_tree, code_string="")

        encoded_strings = np.array(encoded_strings, dtype=str)
        encoded_strings = np.array(
            [np.array([pair[0].zfill(3), pair[1]]) for pair in encoded_strings]
        )
        encoded_strings = encoded_strings[np.argsort(encoded_strings[:, 0])]
        # for symb, string in encoded_strings:
        #     logger.debug(f"VALUE {symb:3} | CODE {string:15}")     
        return encoded_strings
    

    @staticmethod
    def codes_as_dict(huffman_codes: np.ndarray) -> dict:
        """Converts np array of huffman optimal codes to dict."""
        return { int(item[0]): item[1] for item in huffman_codes }


    @classmethod
    def encode(cls, bgr_channels: Tuple[np.ndarray]) -> None:
        """Returns the file according to the huffman tree codes."""
        # Add separator symbol to freqs, represented by 256
        # bgr_channels = tuple(np.append(ch, 256) for ch in bgr_channels)

        # Generate histogram frequencies for each channel
        blue_hist  = sampling.histogram(bgr_channels[0])
        green_hist = sampling.histogram(bgr_channels[1])
        red_hist   = sampling.histogram(bgr_channels[2])

        # Generate Huffman Tree for each channel freq list
        b_ch_htree = cls.generate_tree(blue_hist)
        g_ch_htree = cls.generate_tree(green_hist)
        r_ch_htree = cls.generate_tree(red_hist)

        # Get the codes for each Huffman Tree
        b_ch_codes = cls.get_codes(b_ch_htree)
        g_ch_codes = cls.get_codes(g_ch_htree)
        r_ch_codes = cls.get_codes(r_ch_htree)

        # # TODO: Save the binary trees
        # # Get the binary representation of the huffman trees
        # b_ch_codes_pkl = pickle.dumps(b_ch_codes)
        # g_ch_codes_pkl = pickle.dumps(g_ch_codes)
        # r_ch_codes_pkl = pickle.dumps(r_ch_codes)

        # Create mapping object to new codes
        b_ch_codes_mapping = cls.codes_as_dict(b_ch_codes)
        g_ch_codes_mapping = cls.codes_as_dict(g_ch_codes)
        r_ch_codes_mapping = cls.codes_as_dict(r_ch_codes)

        encoded_b_channel = [
            b_ch_codes_mapping[item] for item in bgr_channels[0]
        ]
        encoded_g_channel = [
            g_ch_codes_mapping[item] for item in bgr_channels[1]
        ]
        encoded_r_channel = [
            r_ch_codes_mapping[item] for item in bgr_channels[2]
        ]

        b_ch_long_bin_string = "".join(encoded_b_channel)
        g_ch_long_bin_string = "".join(encoded_g_channel)
        r_ch_long_bin_string = "".join(encoded_r_channel)

        print(cls.get_size_of(b_ch_long_bin_string))

        final_obj = {
            42: {
                "t_c": b_ch_codes,
                "v": b_ch_long_bin_string
            },
            71: {
                "t_c": g_ch_codes,
                "v": g_ch_long_bin_string   
            },
            82: {
                "t_c": r_ch_codes,
                "v": r_ch_long_bin_string
            }
        }

        return final_obj

        

    @staticmethod
    def convert_chain_to_bytes(bin_repr: str) -> bytes:
        bytes_repr = int(bin_repr, 2)
        bytes_repr = bytes_repr(bytes_repr.bit_length()+7, byteorder="big")
        return bytes_repr
    

    @staticmethod
    def get_size_of(bin_repr: str) -> int:
        sizes = []
        for ch in bin_repr:
            sizes.append(sys.getsizeof(ch))
        return sum(sizes)