# Ciphering

## Text to Binary (ASCII)

`utils/text_to_binary.py` converts ASCII text to an 8-bit, space-separated binary string (one byte per character). It accepts only ASCII input; non-ASCII characters raise an error.

### Command line

```bash
python utils/text_to_binary.py "Hola"
```

Output:

```text
01001000 01101111 01101100 01100001
```

### ASCII reference

For the ASCII character table, see https://www.ascii-code.com/.

## Base64 to Binary

`utils/text_to_binary.py` also converts Base64-encoded text to its binary representation using **6 bits per character** (not 8 bits like ASCII). This implements true Base64 decoding:

- Each Base64 character represents a value between **0 and 63**
- Each value is converted to **exactly 6 bits**
- Padding characters (`=`) are removed before conversion

### Base64 Character Mapping

| Range | Values | Description |
|-------|--------|-------------|
| A-Z   | 0-25   | Uppercase letters |
| a-z   | 26-51  | Lowercase letters |
| 0-9   | 52-61  | Digits |
| +     | 62     | Plus sign |
| /     | 63     | Forward slash |
| =     | N/A    | Padding (ignored) |

### Command line

```bash
python utils/text_to_binary.py --base64 "TQ=="
```

Output:

```text
010011010000
```

### More examples

```bash
python utils/text_to_binary.py --base64 "SGk="
# Output: 010010000110100100

python utils/text_to_binary.py --base64 "SG9sYQ=="
# Output: 010010000110111101101100011000010000
```

### How it works

1. **Remove padding**: `TQ==` → `TQ`
2. **Convert each character to 6-bit binary**:
   - `T` (value 19) → `010011`
   - `Q` (value 16) → `010000`
3. **Concatenate**: `010011010000`

## Tests

From the project root, run:

```bash
python -m unittest discover -s tests
```

### Run specific tests

```bash
# Test Base64 to binary conversion
python -m unittest tests.test_text_to_binary.TestBase64ToBinary -v

# Test 6-bit binary conversion
python -m unittest tests.test_number_to_binary.TestDecimalToBinary6 -v
```
