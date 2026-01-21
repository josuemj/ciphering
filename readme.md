# Ciphering

## Text to Binary

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
