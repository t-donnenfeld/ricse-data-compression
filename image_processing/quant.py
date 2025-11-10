import numpy as np

def quantize_midrise_lower(img_array, step):
    return (img_array // step) * step

def quantize_midrise_mid_quantization_indexes(img_array, step):
    return (img_array // step) * step + step // 2

def quantize_midrise_mid(img_array, step):
    return (img_array // step) * step + step // 2

def quantize_midtread_mid(img_array, step):
    return np.round(img_array / step) * step

def mse(original, quantized):
    return np.mean((original - quantized) ** 2)

def deadzone_quantize(x, delta, dz=None):
    x = np.asarray(x)
    if dz is None:
        dz = delta / 2.0
    q = np.sign(x) * np.maximum(0, np.floor(((np.abs(x) - (dz / 2)) / delta) + 1))
    return q