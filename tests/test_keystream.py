import unittest

from utils.keystream.keystream import generate_prng_keystream


class TestKeystreamPRNG(unittest.TestCase):

    def test_same_seed_produces_same_keystream_str_seed(self) -> None:
        seed = "mi-clave"
        stream_1 = generate_prng_keystream(seed, 32)
        stream_2 = generate_prng_keystream(seed, 32)
        self.assertEqual(stream_1, stream_2)

    def test_same_seed_produces_same_keystream_int_seed(self) -> None:
        seed = 2026
        stream_1 = generate_prng_keystream(seed, 40)
        stream_2 = generate_prng_keystream(seed, 40)
        self.assertEqual(stream_1, stream_2)

    def test_different_seed_produces_different_keystream(self) -> None:
        stream_1 = generate_prng_keystream("clave-a", 48)
        stream_2 = generate_prng_keystream("clave-b", 48)
        self.assertNotEqual(stream_1, stream_2)

    def test_keystream_length_equals_requested_length(self) -> None:
        self.assertEqual(len(generate_prng_keystream("abc", 1)), 1)
        self.assertEqual(len(generate_prng_keystream("abc", 10)), 10)
        self.assertEqual(len(generate_prng_keystream("abc", 128)), 128)

    def test_keystream_can_be_greater_than_message_length(self) -> None:
        message = "HOLA"
        stream = generate_prng_keystream("seed", len(message) + 5)
        self.assertGreaterEqual(len(stream), len(message))

    def test_output_is_ascii_range(self) -> None:
        stream = generate_prng_keystream("ascii-seed", 256)
        for char in stream:
            self.assertTrue(0 <= ord(char) <= 127)

    def test_invalid_seed_type_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            generate_prng_keystream(3.14, 10)

    def test_empty_string_seed_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            generate_prng_keystream("", 10)

    def test_invalid_length_type_raises_type_error(self) -> None:
        with self.assertRaises(TypeError):
            generate_prng_keystream("seed", "10")

    def test_invalid_length_value_raises_value_error(self) -> None:
        with self.assertRaises(ValueError):
            generate_prng_keystream("seed", 0)
        with self.assertRaises(ValueError):
            generate_prng_keystream("seed", -5)


if __name__ == "__main__":
    unittest.main()
