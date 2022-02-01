"""Logic related to the Huffman Coding process."""
from typing import Any
from loguru import logger

import numpy as np


class Node:
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
        if self.left_child and self.right_child:
            return f"{{ P: {self.prob:5} | S: {self.symbol:3} | LC: {self.left_child} | RC: {self.right_child}}}"
        elif self.left_child:
            return f"{{ P: {self.prob:5} | S: {self.symbol:3} | LC: {self.left_child} }}"
        elif self.right_child:
            return f"{{ P: {self.prob:5} | S: {self.symbol:3} | RC: {self.right_child} }}"
        else:
            return f"{{ P: {self.prob:5} | S: {self.symbol:3} }}"
    
    def __lt__(self, other: Any) -> bool:
        return self.prob < other.prob 


class HuffmanCoding:

    @staticmethod
    def generate_tree(freqs: np.ndarray) -> None:
        logger.debug(f"SUM FREQS: {np.sum(freqs)}")

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

        logger.debug("HUFFMAN TREE")
        logger.debug(priority_queue)
        
        return priority_queue
