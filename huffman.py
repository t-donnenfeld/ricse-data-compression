import numpy as np
import heapq
from typing import Dict, Tuple, Any


class Node:
    def __init__(self, symbol: Any = None, freq: float = 0.0):
        self.symbol = symbol
        self.freq = freq
        self.left: "Node | None" = None
        self.right: "Node | None" = None

    def __lt__(self, other: "Node") -> bool:
        return self.freq < other.freq


def build_tree(freqs: Dict[Any, int]) -> Node:
    heap: list[Node] = [Node(sym, f) for sym, f in freqs.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        parent = Node(None, left.freq + right.freq)
        parent.left = left
        parent.right = right
        heapq.heappush(heap, parent)

    return heap[0]


def generate_huffman_codes(
    node: Node, prefix: str = "", codes: Dict[Any, str] | None = None
) -> Dict[Any, str]:
    if codes is None:
        codes = {}
    if node.symbol is not None:
        codes[node.symbol] = prefix or "0"
    else:
        if node.left:
            generate_huffman_codes(node.left, prefix + "0", codes)
        if node.right:
            generate_huffman_codes(node.right, prefix + "1", codes)
    return codes


def huffman_from_array(arr: np.ndarray) -> Tuple[Dict[Any, str], float]:
    values, counts = np.unique(arr, return_counts=True)
    freqs = dict(zip(values.tolist(), counts.tolist()))
    total = counts.sum()
    root = build_tree(freqs)
    codes = generate_huffman_codes(root)
    avg_length = sum((len(codes[v]) * (freqs[v] / total)) for v in values)
    return codes, avg_length
