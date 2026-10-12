import unittest

from cryptopals.set01.challenge01 import hex_to_base64


class Challenge01Tests(unittest.TestCase):
    @unittest.skip("Implement challenge 1, then remove this decorator")
    def test_hex_to_base64(self):
        self.assertEqual(hex_to_base64("68656c6c6f"), "aGVsbG8=")
