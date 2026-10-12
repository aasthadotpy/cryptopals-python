import unittest

from cryptopals.set01.challenge02 import fixed_xor


class Challenge02Tests(unittest.TestCase):
    @unittest.skip("Implement challenge 2, then remove this decorator")
    def test_fixed_xor(self):
        self.assertEqual(fixed_xor(bytes.fromhex("0f00"), bytes.fromhex("f00f")), bytes.fromhex("ff0f"))
