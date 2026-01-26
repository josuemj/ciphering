def xor(bin1 : str, bin2 : str) -> str:
    """Returns the XOR of a two binary strings.

    Args:
        bin1 (str): The first binary string.
        bin2 (str): The second binary string.

    Returns:
        str: The XOR of the two binary strings.
    """
    
    if len(bin1) != len(bin2):
        raise ValueError("Input binary strings must be of the same length.")
    result = ""
    
    for bit1, bit2 in zip(bin1, bin2):
        operator  = int(bit1) ^ int(bit2)
        result += str(operator)
    return result