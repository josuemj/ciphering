from utils.binary_to_decimal import binary_to_decimal

from utils.text_to_binary import ASCII_DICT

# Reverse mapping: decimal value to ASCII character
DECIMAL_TO_ASCII = {v: k for k, v in ASCII_DICT.items()}


def bin_to_ascii(binary_string: str) -> str:
    """Convert a binary string to its ASCII representation.

    Args:
        binary_string (str): A string containing binary digits (0s and 1s).
                            Can be space-separated (e.g., "01001000 01101001")
                            or continuous (e.g., "0100100001101001").
                            Must have a total length divisible by 8.

    Returns:
        str: The ASCII representation of the binary string.
        
    Raises:
        TypeError: If binary_string is not a string
        ValueError: If binary_string length is not divisible by 8 or contains invalid characters
        
    Examples:
        >>> bin_to_ascii("01001000 01101001")
        'Hi'
        >>> bin_to_ascii("0100100001101001")
        'Hi'
    """
    if not isinstance(binary_string, str):
        raise TypeError("binary_string must be a string")
    
    clean_binary = binary_string.replace(" ", "")

    if len(clean_binary) % 8 != 0:
        raise ValueError("binary string length must be divisible by 8")

    # Validate that string contains only 0s and 1s
    if not all(c in '01' for c in clean_binary):
        raise ValueError("binary string must contain only 0s and 1s")

    ascii_string = ""
    
    for i in range(0, len(clean_binary), 8):
        # Get the 8-bit segment
        binary_segment = clean_binary[i:i+8]
        # Convert to decimal
        decimal_value = binary_to_decimal(binary_segment)

        ascii_char = DECIMAL_TO_ASCII[decimal_value]
        ascii_string += ascii_char

    
    return ascii_string