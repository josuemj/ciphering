"""Binary to decimal conversion utilities.

This module provides functions for converting binary strings to decimal values,
specifically designed for Base64 encoding/decoding operations.
"""


def binary6_to_decimal(binary_str: str) -> int:
    """Convert a 6-bit binary string to its decimal value (0-63).
    
    This function is specifically designed for Base64 encoding, where each
    group of 6 bits is converted to a decimal value between 0 and 63.
    
    Args:
        binary_str: A 6-character string containing only '0' and '1'
        
    Returns:
        Integer value in range 0-63
        
    Raises:
        TypeError: If binary_str is not a string
        ValueError: If binary_str is not exactly 6 characters or contains
                   characters other than '0' or '1'
                   
    Examples:
        >>> binary6_to_decimal("000000")
        0
        >>> binary6_to_decimal("111111")
        63
        >>> binary6_to_decimal("010011")
        19
    """
    if not isinstance(binary_str, str):
        raise TypeError("binary_str must be a string")
    
    if len(binary_str) != 6:
        raise ValueError(f"binary_str must be exactly 6 characters, got {len(binary_str)}")
    
    # Validate characters
    for char in binary_str:
        if char not in ('0', '1'):
            raise ValueError(f"binary_str must contain only '0' or '1', got '{char}'")
    
    # Manual conversion: binary to decimal
    # Each position represents a power of 2: 2^5, 2^4, 2^3, 2^2, 2^1, 2^0
    decimal_value = 0
    for i, bit in enumerate(binary_str):
        if bit == '1':
            # Position 0 is the most significant bit (2^5)
            power = 5 - i
            decimal_value += 2 ** power
    
    return decimal_value


def binary_to_decimal(binary_str: str) -> int:
    """Convert a binary string of any length to its decimal value.
    
    Args:
        binary_str: A string containing only '0' and '1'
        
    Returns:
        Integer decimal value
        
    Raises:
        TypeError: If binary_str is not a string
        ValueError: If binary_str is empty or contains characters other than '0' or '1'
                   
    Examples:
        >>> binary_to_decimal("00000000")
        0
        >>> binary_to_decimal("11111111")
        255
        >>> binary_to_decimal("01000001")
        65
    """
    if not isinstance(binary_str, str):
        raise TypeError("binary_str must be a string")
    
    if len(binary_str) == 0:
        raise ValueError("binary_str cannot be empty")
    
    # Validate characters
    for char in binary_str:
        if char not in ('0', '1'):
            raise ValueError(f"binary_str must contain only '0' or '1', got '{char}'")
    
    # Manual conversion: binary to decimal
    decimal_value = 0
    length = len(binary_str)
    for i, bit in enumerate(binary_str):
        if bit == '1':
            power = length - 1 - i
            decimal_value += 2 ** power
    
    return decimal_value
