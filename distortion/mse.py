import numpy as np

def get_mse(original, compressed):
    return np.mean((original - compressed) ** 2)

