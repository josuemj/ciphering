from utils.binary_to_decimal import binary6_to_decimal
from utils.base64_utils import get_base64_char


def binary_to_base64(binary_str: str) -> str:
    """Convert binary string to Base64 text using 6 bits per character.
    
    This function converts a binary string to its Base64 representation.
    The binary string is processed in chunks of 6 bits, each of which is
    converted to a Base64 character. If the length of the binary string
    is not a multiple of 6, it is padded with zeros at the end.
    
    Args:
        binary_str: Binary string representation (may not be multiple of 6 bits)
        
    Returns:
        Base64-encoded string
        
    Raises:
        TypeError: If binary_str is not a string
        ValueError: If binary_str contains characters other than '0' or '1'
        
    Examples:
        >>> binary_to_base64("010011010000")
        'TQ'
        >>> binary_to_base64("010010000110110001101001")
        'SGk'
    """
    # Validate input type
    if not isinstance(binary_str, str):
        raise TypeError("binary_str must be a string")
    
    # Handle empty string
    if len(binary_str) == 0:
        return ""
    
    # Validate characters
    for char in binary_str:
        if char not in ('0', '1'):
            raise ValueError(f"binary_str must contain only '0' or '1', got '{char}'")
    
    # Pad binary string to make length a multiple of 6
    padding_needed = (6 - len(binary_str) % 6) % 6
    padded_binary = binary_str + '0' * padding_needed
    
    # Split into groups of 6 bits
    base64_chars = []
    for i in range(0, len(padded_binary), 6):
        six_bits = padded_binary[i:i+6]
        
        # Convert 6 bits to decimal (0-63)
        decimal_value = binary6_to_decimal(six_bits)
        
        # Convert decimal to Base64 character
        base64_char = get_base64_char(decimal_value)
        base64_chars.append(base64_char)
    
    return "".join(base64_chars)