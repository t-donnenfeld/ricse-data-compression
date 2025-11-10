import entro
import huffman
import image
import ac
import numpy as np


def exam_question_b():
    flower = image.RawImage("./data/flower-bsq-u8be-3x1512x2268.raw", 2268, 1512, 3)
    print("Computing entropies (in bits)...")

    H_total = entro.get_entropy_from_array(flower.data)
    H_channels = [
        entro.get_entropy_from_array(flower.data[c]) for c in range(flower.channel_nbr)
    ]

    print(f"Global entropy: {H_total:.4f} bits")
    for i, H in enumerate(H_channels):
        print(f"Channel {i}: {H:.4f} bits")


def exam_question_d():
    flower = image.RawImage("./data/flower-bsq-u8be-3x1512x2268.raw", 2268, 1512, 3)
    H_before = entro.get_entropy_from_array(flower.data)
    flower.set_value(0, 0, 0, 0x00)
    flower.set_value(flower.width - 1, flower.height - 1, 0, 0xFF)
    flower.add_ppm_header("./data/flower_ppm_header.txt")
    H_after = entro.get_entropy_from_array(flower.data)
    print(f"Delta Entropy after adding header: {H_before - H_after} bits")


def exam_question_e():
    flower_8 = image.RawImage("./data/flower-bsq-u8be-3x1512x2268.raw", 2268, 1512, 3)
    flower_le = image.RawImage("./data/flower-bsq-u8be-3x1512x2268.raw", 2268, 1512, 3)
    flower_be = image.RawImage("./data/flower-bsq-u8be-3x1512x2268.raw", 2268, 1512, 3)

    flower_le.to_higher_sample_size(2, "little")
    flower_be.to_higher_sample_size(2, "big")

    flower_le.set_value(0, 0, 0, 0x0000)
    flower_le.set_value(flower_le.width - 1, flower_le.height - 1, 0, 0xFFFF)
    flower_be.set_value(0, 0, 0, 0x0000)
    flower_be.set_value(flower_be.width - 1, flower_be.height - 1, 0, 0xFFFF)

    H8 = entro.get_entropy_from_array(flower_8.data)
    Hle = entro.get_entropy_from_array(flower_le.data)
    Hbe = entro.get_entropy_from_array(flower_be.data)
    print(f"Entropy diff 8-bit -> 16-bit LE: {H8 - Hle} bits")
    print(f"Entropy diff 8-bit -> 16-bit BE: {H8 - Hbe} bits")

    hc = huffman.huffman_code_from_array(flower_8.data)

    print(hc)

def old():
    flower_8 = image.RawImage("./data/flower-bsq-u8be-3x1512x2268.raw", 2268, 1512, 3)
    hist = flower_8.get_bytes_histogram()
    max = 0
    sum = 0
    for k, v in hist.items():
        sum += v
        if v > max:
            max = v
        print(f"{k}: {v}, {max}")
    print(max / sum)
    flower_8 = image.RawImage("./data/flower-bsq-u8be-3x1512x2268.raw", 2268, 1512, 3)
    _, counts = np.unique(flower_8.data, return_counts=True)
    probabilities = counts / counts.sum()
    code_value = ac.arithmetic_encode([int(k) for k in flower_8.data.ravel()], probabilities)
    print(len(flower_8.data.ravel()))
    print(code_value)

    ## Components
    mandrill = image.RawImage("./data/mandrill-u8be-3x512x512.raw", 512, 512, 3)
    for i in range(8):
        mandrill.write_black_and_white_bitplane_component(i, "./data/out/mandrill_" + str(i) + ".raw")



if __name__ == "__main__":
    geo = image.RawImage("./data/Geo_Sample-u16be-242x1024x256.raw", 1024, 256, 242, sample_size=2)
    print(entro.get_entropy_from_array(geo.data))



