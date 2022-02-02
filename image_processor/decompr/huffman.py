"""Logic related to the Huffman Coding process."""
from typing import Any, List
from loguru import logger

from pprint import pprint

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
                symbol: Any="",
                left_child: Any=None,
                right_child: Any=None) -> None:
        self.prob = prob
        self.symbol = symbol
        self.left_child = left_child
        self.right_child = right_child
        self.code = ''
    
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
        # logger.debug(f"SUM FREQS: {np.sum(freqs)}")

        # Assemble a priority queue ordered by freqs
        priority_list = np.array([(i, f) for i, f in enumerate(freqs)])
        priority_list = priority_list[np.argsort(priority_list[:, 1])]

        # At this point this list is supposed to be sorted by probability/freq
        priority_queue = [ Node(prob=fq, symbol=symb) for symb, fq in priority_list ]

        # priority_queue = priority_queue[:7] # TODO: Remove this crop

        while len(priority_queue) > 1:
            # Initial length of priority queue
            ini_length_pqueue = len(priority_queue)

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

            assert ini_length_pqueue > len(priority_queue)

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

            if node.symbol:
                encoded_strings.append(
                    [node.symbol, code_string]
                )
                code_string = code_string[:-1]
        
        dfs_traverse(huffman_tree, code_string="")


        encoded_strings = np.array(encoded_strings, dtype=np.int)
        encoded_strings = encoded_strings[np.argsort(encoded_strings[:, 0])]

        for symb, string in encoded_strings:
            logger.debug(f"VALUE {symb:3} | CODE {int(string):15}")
        
        return encoded_strings
