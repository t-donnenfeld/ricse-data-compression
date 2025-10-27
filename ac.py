import numpy as np

def arithmetic_encode(sequence, probs):
    low, high = 0.0, 1.0
    cum_high = np.cumsum(probs)
    cum_low = np.concatenate(([0.0], cum_high[:-1]))
    counter = 0
    for s in sequence:
        rng = high - low
        high = low + rng * cum_high[s]
        low = low + rng * cum_low[s]
        if high - low > 0:
            print(f"Interval size {high - low} at {counter}")
        counter += 1

    return (low + high) / 2 # arbitrary


def arithmetic_decode(code_value, probs, length):
    result = []
    low, high = 0.0, 1.0
    cum_high = np.cumsum(probs)
    cum_low = np.concatenate(([0.0], cum_high[:-1]))

    for _ in range(length):
        rng = high - low
        scaled_value = (code_value - low) / rng

        s = np.searchsorted(cum_high, scaled_value)
        result.append(s)

        high = low + rng * cum_high[s]
        low = low + rng * cum_low[s]

    return result
