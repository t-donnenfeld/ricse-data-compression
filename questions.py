import image
import entro


def exam_question_e():
    flower_8 = image.RawImage("./data/flower-bsq-u8be-3x1512x2268.raw", 2268, 1512, 3)
    flower = image.RawImage("./data/flower-bsq-u8be-3x1512x2268.raw", 2268, 1512, 3)
    flower2 = image.RawImage("./data/flower-bsq-u8be-3x1512x2268.raw", 2268, 1512, 3)
    print(len(flower.data))
    flower.to_higher_sample_size(2, "little")
    flower2.to_higher_sample_size(2, "big")

    print(len(flower.data))
    flower.set_value(0, 0, 0, 0)
    flower2.set_value(0, 0, 0, 0)
    # flower.set_value(2268, 1512, 2, 65535)
    # flower2.set_value(2268, 1512, 2, 65535)
    flower.data[-1] = 255
    flower.data[-2] = 255
    flower2.data[-1] = 255
    flower2.data[-2] = 255

    p8bytes = entro.histogram_dict_to_unordered_probabilities(
        flower_8.get_bytes_histogram()
    )

    p1 = entro.histogram_dict_to_unordered_probabilities(flower.get_bytes_histogram())
    p2 = entro.histogram_dict_to_unordered_probabilities(flower2.get_bytes_histogram())
    print(entro.get_entropy(p8bytes) - entro.get_entropy(p1))
    print(entro.get_entropy(p8bytes) - entro.get_entropy(p2))

    flower.write("flower_2bytes_le.raw")
    flower2.write("flower_2bytes_be.raw")


def exam_question_d():
    flower = image.RawImage("./data/flower-bsq-u8be-3x1512x2268.raw", 2268, 1512, 3)
    hist_before = flower.get_bytes_histogram()
    # flower.to_BIP()
    flower.add_ppm_header("./data/flower_ppm_header.txt")
    hist_after = flower.get_bytes_histogram()
    p1 = entro.histogram_dict_to_unordered_probabilities(hist_before)
    p2 = entro.histogram_dict_to_unordered_probabilities(hist_after)
    print(entro.get_entropy(p1) - entro.get_entropy(p2))
    # flower.write("./out.ppm")


def exam_question_b():
    flower = image.RawImage("./data/flower-bsq-u8be-3x1512x2268.raw", 2268, 1512, 3)
    hist = flower.get_bytes_histogram()
    hist1 = flower.get_bytes_histogram_of_channel(0)
    hist2 = flower.get_bytes_histogram_of_channel(1)
    hist3 = flower.get_bytes_histogram_of_channel(2)
    probas = entro.histogram_dict_to_unordered_probabilities(hist)
    probas1 = entro.histogram_dict_to_unordered_probabilities(hist1)
    probas2 = entro.histogram_dict_to_unordered_probabilities(hist2)
    probas3 = entro.histogram_dict_to_unordered_probabilities(hist3)
    print(entro.get_entropy(probas))
    print(entro.get_entropy(probas1))
    print(entro.get_entropy(probas2))
    print(entro.get_entropy(probas3))


if __name__ == "__main__":
    exam_question_e()
