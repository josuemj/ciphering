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
