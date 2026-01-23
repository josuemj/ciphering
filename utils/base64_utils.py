"""Base64 utility mappings and constants.

This module provides the decimal to Base64 character mapping used for
encoding binary data to Base64 format.
"""

# Base64 character set: A-Z (0-25), a-z (26-51), 0-9 (52-61), + (62), / (63)
DECIMAL_TO_BASE64 = {}

# A-Z → 0-25
for i in range(26):
    DECIMAL_TO_BASE64[i] = chr(ord('A') + i)

# a-z → 26-51
for i in range(26):
    DECIMAL_TO_BASE64[26 + i] = chr(ord('a') + i)

# 0-9 → 52-61
for i in range(10):
    DECIMAL_TO_BASE64[52 + i] = chr(ord('0') + i)

# Special characters
DECIMAL_TO_BASE64[62] = '+'
DECIMAL_TO_BASE64[63] = '/'

# Padding character
BASE64_PADDING = '='


def get_base64_char(decimal_value: int) -> str:
    """Get the Base64 character for a decimal value (0-63).
    
    Args:
        decimal_value: Integer in range 0-63
        
    Returns:
        Corresponding Base64 character
        
    Raises:
        TypeError: If decimal_value is not an integer
        ValueError: If decimal_value is not in range 0-63
    """
    if not isinstance(decimal_value, int):
        raise TypeError("decimal_value must be an integer")
    
    if decimal_value < 0 or decimal_value > 63:
        raise ValueError(f"decimal_value must be in range 0-63, got {decimal_value}")
    
    return DECIMAL_TO_BASE64[decimal_value]
