"""
Prompt:
Implement a function that generates a pseudo-random keystream for stream-cipher
practice. The solution must:
1. Use a basic pseudo-random number generator (PRNG).
2. Accept a key (seed) as the initialization parameter.
3. Generate a keystream with length equal to or greater than the message length.
4. Be deterministic: the same seed must always produce the same keystream.
"""


def _seed_to_int(seed: str | int, modulus: int) -> int:
    """Convert a seed (string or integer) to a deterministic integer state."""
    if isinstance(seed, int):
        value = seed % modulus
        return value if value != 0 else 1

    if isinstance(seed, str):
        if len(seed) == 0:
            raise ValueError("seed string cannot be empty")

        value = 0
        for index, char in enumerate(seed):
            value = (value * 131 + ord(char) + index) % modulus
        return value if value != 0 else 1

    raise TypeError("seed must be a string or an integer")


def generate_prng_keystream(seed: str | int, length: int) -> str:
    """Generate a deterministic pseudo-random keystream.

    Uses a basic LCG (Linear Congruential Generator) as PRNG:
    X(n+1) = (a * X(n) + c) mod m

    Args:
        seed: Seed value used to initialize the PRNG state.
        length: Desired keystream length. Use len(message) or greater.

    Returns:
        A pseudo-random ASCII keystream string of requested length.

    Raises:
        TypeError: If length is not int or seed has invalid type.
        ValueError: If length < 1 or seed string is empty.
    """
    if not isinstance(length, int):
        raise TypeError("length must be an integer")
    if length < 1:
        raise ValueError("length must be at least 1")

    # LCG parameters (common set used in basic PRNG examples)
    modulus = 2**31
    multiplier = 1103515245
    increment = 12345

    state = _seed_to_int(seed, modulus)
    output = []

    for _ in range(length):
        state = (multiplier * state + increment) % modulus
        output.append(chr(state % 128))

    return "".join(output)
