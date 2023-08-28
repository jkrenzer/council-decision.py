from unittest import TestCase

from council_decision.crypto.key_ring import KeyRing
from council_decision.crypto.plain_text import PlainText
from council_decision.crypto import InvalidSignature


class TestKeyRing(TestCase):
    def test_creation(self):
        key_ring = KeyRing()
        self.assertIsInstance(key_ring, KeyRing)

    def test_import_export(self):
        key_ring = KeyRing()
        key_ring_dump = key_ring.model_dump()
        key_ring2 = KeyRing(**key_ring_dump)
        self.assertEqual(key_ring, key_ring2)

    def test_encryption(self):
        key_ring = KeyRing()
        plain_text = PlainText(data=b"A very secret message!")
        cipher_text = key_ring.encrypt(plain_text)
        self.assertNotEqual(plain_text.data, cipher_text.data)
        plain_text2 = key_ring.decrypt(cipher_text)
        self.assertEqual(plain_text.data, plain_text2.data)

    def test_signing(self):
        key_ring = KeyRing()
        plain_text = PlainText(data=b"A very secret message!")
        signature = key_ring.sign(plain_text)
        key_ring.verify(signature, plain_text)
        plain_text2 = PlainText(data=b"A very secret message?")
        with self.assertRaises(InvalidSignature):
            key_ring.verify(signature, plain_text2)
