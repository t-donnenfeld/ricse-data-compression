import numpy as np

symbols = np.array([0, 1, 2, 3])
probs = np.array([0.322043, 0.318395, 0.24544, 0.114122])

def arithmetic_encode(sequence, probs):
    low, high = 0.0, 1.0
    cum_high = np.cumsum(probs)
    cum_low = np.concatenate(([0.0], cum_high[:-1]))

    for s in sequence:
        rng = high - low
        high = low + rng * cum_high[s]
        low = low + rng * cum_low[s]
        print(f"Encoded {s}: [{low:.9f}, {high:.9f}]")
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


sequence = [3, 3, 2]
print("Encoding sequence:", sequence)

code_value = arithmetic_encode(sequence, probs)
print(f"\nFinal code value: {code_value:.12f}")

decoded = arithmetic_decode(code_value, probs, len(sequence))
print("\nDecoded sequence:", decoded)