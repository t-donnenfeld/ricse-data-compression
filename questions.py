import image
import entro


def exam_question_d():
    flower = image.RawImage(
        "./data/flower-bsq-u8be-3x1512x2268.raw", 2268, 1512, 3, "u8be"
    )
    hist_before = flower.get_bytes_histogram()
    flower.to_BIP()
    flower.add_ppm_header("./data/flower_ppm_header.txt")
    hist_after = flower.get_bytes_histogram()
    p1 = entro.histogram_dict_to_unordered_probabilities(hist_before)
    p2 = entro.histogram_dict_to_unordered_probabilities(hist_after)
    print(entro.get_entropy(p1) - entro.get_entropy(p2))
    # flower.write("./out.ppm")


def exam_question_b():
    flower = image.RawImage(
        "./data/flower-bsq-u8be-3x1512x2268.raw", 2268, 1512, 3, "u8be"
    )
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
    exam_question_d()
