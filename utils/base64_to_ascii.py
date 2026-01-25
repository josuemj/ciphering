"""Utilities for converting Base64 strings back to ASCII text."""

from utils.binary_to_decimal import binary_to_decimal
from utils.text_to_binary import ASCII_DICT, base64_to_binary

ASCII_DECIMAL_TO_CHAR = {value: char for char, value in ASCII_DICT.items()}


def base64_to_ascii(base64_str: str) -> str:
    """Decode a Base64 string into its ASCII representation.
    
    Args:
        base64_str: Base64-encoded string (may include padding characters)

    Returns:
        Decoded ASCII text

    Raises:
        TypeError: If base64_str is not a string
        ValueError: If the decoded bitstream cannot be grouped into 8-bit bytes
                    or produces values outside the ASCII range
    """
    if not isinstance(base64_str, str):
        raise TypeError("base64_str must be a string")

    binary_stream = base64_to_binary(base64_str)

    # Base64 padding (= or ==) indicates that 2 or 4 bits at the end
    padding_length = len(base64_str) - len(base64_str.rstrip('='))
    if padding_length:
        bits_to_trim = padding_length * 2
        if bits_to_trim >= len(binary_stream):
            binary_stream = ""
        else:
            binary_stream = binary_stream[:-bits_to_trim]

    if not binary_stream:
        return ""

    if len(binary_stream) % 8 != 0:
        raise ValueError("Invalid Base64 input: bit stream is not byte-aligned")

    ascii_chars = []
    for i in range(0, len(binary_stream), 8):
        byte_bits = binary_stream[i:i + 8]
        decimal_value = binary_to_decimal(byte_bits)

        if decimal_value not in ASCII_DECIMAL_TO_CHAR:
            raise ValueError(
                f"Invalid decimal value {decimal_value} - outside ASCII range 0-127"
            )

        ascii_chars.append(ASCII_DECIMAL_TO_CHAR[decimal_value])

    return "".join(ascii_chars)