from utils.number_to_binary import decimal_to_binary

# Manual ASCII dictionary mapping all ASCII characters (0-127) to their decimal values
ASCII_DICT = {chr(i): i for i in range(128)}


def text_to_binary(text: str) -> str:
    """Convert ASCII text to a space-separated binary string (8 bits per byte)."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    
    binary_parts = []
    for char in text:
        if char not in ASCII_DICT:
            raise ValueError(f"Invalid character '{char}' - must contain only ASCII characters (0-127)")
        
        ascii_value = ASCII_DICT[char]
        binary_str = decimal_to_binary(ascii_value)
        binary_parts.append(binary_str)
    
    return " ".join(binary_parts)

    
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python text_to_binary.py <text>")
        raise SystemExit(2)

    print(text_to_binary(" ".join(sys.argv[1:])))
