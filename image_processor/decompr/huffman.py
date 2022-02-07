"""Logic related to the Huffman Coding process."""
from typing import Any, List, Tuple
from image_processor.core import sampling

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


class HuffmanCoding:

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
        encoded_strings = encoded_strings[np.argsort(encoded_strings[:, 0])]

        # for symb, string in encoded_strings:
        #     logger.debug(f"VALUE {symb:3} | CODE {string:15}")
        
        return encoded_strings


    @classmethod
    def encode(cls, bgr_channels: Tuple[np.ndarray]) -> None:
        """Returns the file according to the huffman tree codes."""
        # Add separator symbol to freqs, represented by 256
        bgr_channels = tuple(np.append(ch, 256) for ch in bgr_channels)
        
        # Generate histogram frequencies for each channel
        blue_hist  = sampling.histogram(bgr_channels[0], L=257)
        green_hist = sampling.histogram(bgr_channels[1], L=257)
        red_hist   = sampling.histogram(bgr_channels[2], L=257)

        # Generate Huffman Tree for each channel freq list
        b_ch_htree = cls.generate_tree(blue_hist)
        g_ch_htree = cls.generate_tree(green_hist)
        r_ch_htree = cls.generate_tree(red_hist)

        # Get the codes that matches the given symbols
        b_ch_codes = cls.get_codes(b_ch_htree)
        g_ch_codes = cls.get_codes(g_ch_htree)
        r_ch_codes = cls.get_codes(r_ch_htree)

        # print(b_ch_codes)

        for element in b_ch_codes:
            if int(element[0]) == 256:
                print(element)

