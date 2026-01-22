def decimal_to_binary(num: int) -> str:
    """Convert a decimal number to an 8-bit binary string using manual division.
    
    Args:
        num: Integer in range 0-255
        
    Returns:
        8-bit binary string representation
        
    Raises:
        ValueError: If num is not in range 0-255
        TypeError: If num is not an integer
    """
    if not isinstance(num, int):
        raise TypeError("num must be an integer")
    
    if num < 0 or num > 255:
        raise ValueError(f"num must be in range 0-255, got {num}")
    
    # Special case for 0
    if num == 0:
        return "00000000"
    
    # Manual division by 2 algorithm
    binary_digits = []
    current = num
    
    while current > 0:
        remainder = current % 2
        binary_digits.append(str(remainder))
        current = current // 2
    
    # Reverse to get correct order (remainders are collected in reverse)
    binary_digits.reverse()
    
    # Pad to 8 bits with leading zeros
    binary_str = "".join(binary_digits)
    while len(binary_str) < 8:
        binary_str = "0" + binary_str
    
    return binary_str


def decimal_to_binary_6(value: int) -> str:
    """Convert a decimal number (0-63) to a 6-bit binary string.
    
    This function is specifically designed for Base64 decoding, where each
    Base64 character represents a value between 0 and 63 (2^6 = 64 values).
    
    Args:
        value: Integer in range 0-63
        
    Returns:
        6-bit binary string representation
        
    Raises:
        ValueError: If value is not in range 0-63
        TypeError: If value is not an integer
        
    Examples:
        >>> decimal_to_binary_6(0)
        '000000'
        >>> decimal_to_binary_6(1)
        '000001'
        >>> decimal_to_binary_6(6)
        '000110'
        >>> decimal_to_binary_6(18)
        '010010'
        >>> decimal_to_binary_6(63)
        '111111'
    """
    if not isinstance(value, int):
        raise TypeError("value must be an integer")
    
    if value < 0 or value > 63:
        raise ValueError(f"value must be in range 0-63, got {value}")
    
    # Special case for 0
    if value == 0:
        return "000000"
    
    # Manual division by 2 algorithm
    binary_digits = []
    current = value
    
    while current > 0:
        remainder = current % 2
        binary_digits.append(str(remainder))
        current = current // 2
    
    # Reverse to get correct order (remainders are collected in reverse)
    binary_digits.reverse()
    
    # Pad to 6 bits with leading zeros
    binary_str = "".join(binary_digits)
    while len(binary_str) < 6:
        binary_str = "0" + binary_str
    
    return binary_str
