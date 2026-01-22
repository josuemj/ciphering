import sys
import os

# Add parent directory to path for imports when running as script
if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.number_to_binary import decimal_to_binary, decimal_to_binary_6

# Manual ASCII dictionary mapping all ASCII characters (0-127) to their decimal values
ASCII_DICT = {chr(i): i for i in range(128)}

# Base64 character to decimal value mapping
# A-Z: 0-25, a-z: 26-51, 0-9: 52-61, +: 62, /: 63
BASE64_DICT = {}

# A-Z → 0-25
for i in range(26):
    BASE64_DICT[chr(ord('A') + i)] = i

# a-z → 26-51
for i in range(26):
    BASE64_DICT[chr(ord('a') + i)] = 26 + i

# 0-9 → 52-61
for i in range(10):
    BASE64_DICT[chr(ord('0') + i)] = 52 + i

# Special characters
BASE64_DICT['+'] = 62
BASE64_DICT['/'] = 63


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


def base64_to_binary(text: str) -> str:
    """Convert Base64 text to binary string using 6 bits per character.
    
    This function converts Base64-encoded text to its binary representation.
    Each Base64 character represents a value between 0 and 63, which is
    converted to a 6-bit binary string. Padding characters (=) are removed
    before conversion as they don't represent actual data.
    
    Args:
        text: Base64-encoded string (may include padding with =)
        
    Returns:
        Binary string representation (6 bits per Base64 character)
        
    Raises:
        TypeError: If text is not a string
        ValueError: If text contains invalid Base64 characters
        
    Examples:
        >>> base64_to_binary("TQ==")
        '010011010000'
        >>> base64_to_binary("SGk=")
        '010010000110110001101001'
    """
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    
    # Step 1: Remove padding (= characters don't represent information)
    text_no_padding = text.rstrip('=')
    
    # Step 2: Convert each Base64 character to binary
    binary_parts = []
    
    for char in text_no_padding:
        # Step 3: Get decimal value (0-63) from Base64 character
        if char not in BASE64_DICT:
            raise ValueError(f"Invalid Base64 character '{char}'")
        
        decimal_value = BASE64_DICT[char]
        
        # Step 4: Convert to 6-bit binary
        binary_str = decimal_to_binary_6(decimal_value)
        
        # Step 5: Concatenate
        binary_parts.append(binary_str)
    
    # Step 6: Return final binary string
    return "".join(binary_parts)

    
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage:")
        print("  python text_to_binary.py <text>           # Convert ASCII text to binary")
        print("  python text_to_binary.py --base64 <text>  # Convert Base64 to binary")
        raise SystemExit(2)

    # Check if --base64 flag is present
    if sys.argv[1] == "--base64":
        if len(sys.argv) < 3:
            print("Error: --base64 requires a Base64 string")
            raise SystemExit(2)
        print(base64_to_binary(" ".join(sys.argv[2:])))
    else:
        print(text_to_binary(" ".join(sys.argv[1:])))
