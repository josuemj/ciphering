# Project Structure

```text
ciphering/
├── ctf-s/
├── img/
├── input/
├── research/
├── tests/
├── utils/
│   ├── analysis/
│   │   └── frequency_analysis.py
│   ├── block/
│   │   ├── aes_ecb_cbc.py
│   │   ├── analysis_report.py
│   │   ├── base.py
│   │   ├── des_ecb.py
│   │   └── triple_des_cbc.py
│   ├── ciphers/
│   │   ├── caesar.py
│   │   ├── rot13.py
│   │   ├── vigere.py
│   │   └── xor_cipher.py
│   ├── entrophy/
│   │   ├── probabilites.py
│   │   ├── relative.py
│   │   └── shanon.py
│   ├── keys/
│   │   └── dynamic_key.py
│   ├── keystream/
│   │   ├── keystream.py
│   │   ├── keystream_cipher.py
│   │   └── keystream_decipher.py
│   ├── base64_to_ascii.py
│   ├── base64_utils.py
│   ├── binary_to_base64.py
│   ├── binary_to_decimal.py
│   ├── bin_to_ascii.py
│   ├── number_to_binary.py
│   ├── text_to_binary.py
│   └── xor.py
├── play.py
└── readme.md
```

# Utils Quick Guide

- `utils/analysis/frequency_analysis.py`: Basic character frequency analysis for ciphertext.
- `utils/block/aes_ecb_cbc.py`: AES demo in ECB and CBC modes.
- `utils/block/analysis_report.py`: Helper to compare/report block mode behavior.
- `utils/block/base.py`: Shared utilities for block cipher scripts.
- `utils/block/des_ecb.py`: DES encryption example in ECB mode.
- `utils/block/triple_des_cbc.py`: 3DES encryption example in CBC mode.
- `utils/ciphers/caesar.py`: Caesar cipher encrypt/decrypt helpers.
- `utils/ciphers/rot13.py`: ROT13 transformation utility.
- `utils/ciphers/vigere.py`: Vigenere cipher implementation.
- `utils/ciphers/xor_cipher.py`: XOR cipher for text/key operations.
- `utils/entrophy/probabilites.py`: Character probability calculations.
- `utils/entrophy/relative.py`: Relative frequency utilities.
- `utils/entrophy/shanon.py`: Shannon entropy calculation.
- `utils/keys/dynamic_key.py`: Dynamic key generation/handling logic.
- `utils/keystream/keystream.py`: Keystream generation core logic.
- `utils/keystream/keystream_cipher.py`: Stream cipher encrypt flow with keystream.
- `utils/keystream/keystream_decipher.py`: Stream cipher decrypt flow with keystream.
- `utils/base64_to_ascii.py`: Converts Base64 to ASCII text.
- `utils/base64_utils.py`: Common Base64 helper functions.
- `utils/binary_to_base64.py`: Converts binary input to Base64.
- `utils/binary_to_decimal.py`: Converts binary input to decimal number.
- `utils/bin_to_ascii.py`: Converts binary bytes to ASCII text.
- `utils/number_to_binary.py`: Converts numbers to binary format.
- `utils/text_to_binary.py`: Converts plain text to binary.
- `utils/xor.py`: Bitwise XOR helper operations.

## Running Tests

```bash
python -m unittest discover -s tests -v
```
