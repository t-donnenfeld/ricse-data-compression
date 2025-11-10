def rice_encode(x: int, k: int) -> str:
    """
    Encode non-negative integer x using Rice coding with parameter k.
    Returns a string of bits, e.g. "11011".
    """
    M = 1 << k
    q = x // M
    r = x % M

    unary = '1' * q + '0'
    binary = format(r, f'0{k}b')
    return unary + binary


def rice_decode(code: str, k: int) -> int:
    """
    Decode a Rice-coded bitstring (no padding).
    Returns the decoded integer x.
    """
    q = 0
    for bit in code:
        if bit == '1':
            q += 1
        else:
            break
    remainder_bits = code[q+1 : q+1+k]
    r = int(remainder_bits, 2)
    return q * (1 << k) + r

if __name__ == "__main__":
    k = 2  # power of two
    for x in range(12):
        code = rice_encode(x, k)
        decoded = rice_decode(code, k)
        print(f"x={x:2d} -> code={code:6s} -> decoded={decoded}")