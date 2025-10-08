import math


def histogram_dict_to_unordered_probabilities(histogram: dict):
    total = sum(histogram.values())
    return [x / total for x in histogram.values()]


def get_self_information_in_bits(probability: float):
    return -1 * math.log2(probability)


def get_entropy(probabilities: list[float]):
    return sum([x * get_self_information_in_bits(x) for x in probabilities])
