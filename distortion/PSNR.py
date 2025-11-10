import numpy as np

def calculate_psnr(original, compressed):
    mse = np.mean((original - compressed) ** 2)

    if mse == 0:
        return float('inf')  # No distortion
    max_pixel_value = 255.0
    psnr = 20 * np.log10(max_pixel_value / np.sqrt(mse))
    return psnr
