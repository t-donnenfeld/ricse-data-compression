import numpy as np


def get_entropy_from_array(arr: np.ndarray) -> float:
    _, counts = np.unique(arr, return_counts=True)
    probabilities = counts / counts.sum()
    entropy = -np.sum(probabilities * np.log2(probabilities))
    return float(entropy)
