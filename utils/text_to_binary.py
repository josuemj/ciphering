def text_to_binary(text: str) -> str:
    """Convert ASCII text to a space-separated binary string (8 bits per byte)."""
    if not isinstance(text, str):
        raise TypeError("text must be a string")
    try:
        ascii_bytes = text.encode("ascii")
    except UnicodeEncodeError as exc:
        raise ValueError("text must contain only ASCII characters") from exc
    return " ".join(f"{byte:08b}" for byte in ascii_bytes)


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python text_to_binary.py <text>")
        raise SystemExit(2)

    print(text_to_binary(" ".join(sys.argv[1:])))
