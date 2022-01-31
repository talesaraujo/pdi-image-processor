"""Logic related to the Huffman Coding process."""
from typing import Any
from image_processor.core.sampling import histogram
import numpy as np


class Node:
    def __init__(self,
                prob: int,
                symbol: Any,
                left_child: Any=None,
                right_child: Any=None) -> None:
        self.prob = prob
        self.symbol = symbol
        self.left_child = left_child
        self.right_child = right_child
        self.code = ''
    
    def __repr__(self) -> str:
        return f"{{ P: {self.prob:5} | S: {self.symbol:3} }}"


class HuffmanCoding:
    @staticmethod
    def encode(freqs: np.ndarray):
        # Assemble a priority queue ordered by freqs
        priority_list = np.array([
            (i, f) for i, f in enumerate(freqs)
        ])
        priority_list = priority_list[np.argsort(priority_list[:, 1])]

        priority_queue = [ Node(prob=fq, symbol=symb) for symb, fq in priority_list ]

        for node in priority_queue:
            print(node)

        
