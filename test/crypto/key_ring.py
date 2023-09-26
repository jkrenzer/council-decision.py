from unittest import TestCase

from council_decision.crypto.dump_password import DumpPassword
from council_decision.crypto.key_ring import (
    PrivateKey,
    PrivateKeyRing,
    LockedPrivateKey,
    LockedPrivateKeyRing,
)
from council_decision.crypto.plain_text import PlainText
from council_decision.crypto import InvalidSignature


class TestKeyRing(TestCase):
    def test_creation(self):
        key_ring = PrivateKeyRing()
        self.assertIsInstance(key_ring, PrivateKeyRing)

    def test_lock_unlock(self):
        key_ring = PrivateKeyRing()
        dump_password = DumpPassword("Test")
        with dump_password:
            locked_key_ring = key_ring.lock()
            self.assertIsInstance(locked_key_ring, LockedPrivateKeyRing)
            self.assertIsInstance(
                locked_key_ring.locked_encryption_key, LockedPrivateKey
            )
            self.assertIsInstance(
                locked_key_ring.locked_signature_key, LockedPrivateKey
            )
            unlocked_key_ring = locked_key_ring.unlock()
            self.assertIsInstance(unlocked_key_ring, PrivateKeyRing)
            self.assertIsInstance(unlocked_key_ring.encrpytion_private_key, PrivateKey)
            self.assertIsInstance(unlocked_key_ring.signature_private_key, PrivateKey)

    def test_import_export(self):
        key_ring = PrivateKeyRing()
        dump_password = DumpPassword("Test")
        with dump_password:
            key_ring_dump = key_ring.model_dump()
        with dump_password:
            key_ring2 = PrivateKeyRing(**key_ring_dump)
        self.assertEqual(key_ring, key_ring2)

    def test_encryption(self):
        key_ring = PrivateKeyRing()
        plain_text = PlainText(data=b"A very secret message!")
        cipher_text = key_ring.encrypt(plain_text)
        self.assertNotEqual(plain_text.data, cipher_text.data)
        plain_text2 = key_ring.decrypt(cipher_text)
        self.assertEqual(plain_text.data, plain_text2.data)

    def test_signing(self):
        key_ring = PrivateKeyRing()
        plain_text = PlainText(data=b"A very secret message!")
        signature = key_ring.sign(plain_text)
        key_ring.verify(signature, plain_text)
        plain_text2 = PlainText(data=b"A very secret message?")
        with self.assertRaises(InvalidSignature):
            key_ring.verify(signature, plain_text2)
