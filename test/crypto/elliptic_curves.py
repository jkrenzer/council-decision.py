from unittest import TestCase


class TestEllipticCurves(TestCase):
    def test_key_generation(self):
        from council_decision.crypto.private_key import EllipticCurvePrivateKey
        from council_decision.crypto.dump_password import DumpPassword

        private_key = EllipticCurvePrivateKey()
        with DumpPassword("Test") as dp:
            serialized = private_key.model_dump()
            private_key2 = EllipticCurvePrivateKey(**serialized)
        self.assertEqual(private_key, private_key2)

    def test_cryptographic_roundtrip(self):
        from council_decision.crypto.private_key import EllipticCurvePrivateKey
        from council_decision.crypto.plain_text import PlainText

        private_key = EllipticCurvePrivateKey()
        plain_text = PlainText(data=b"A very secret message")
        cipher_text = plain_text.encrypt(private_key, private_key.public_key())
        self.assertNotEqual(plain_text, cipher_text)
        plain_text2 = cipher_text.decrypt(private_key, private_key.public_key())
        self.assertEqual(plain_text, plain_text2)

    def test_ciphertext_randomness(self):
        from council_decision.crypto.private_key import EllipticCurvePrivateKey
        from council_decision.crypto.plain_text import PlainText

        private_key = EllipticCurvePrivateKey()
        plain_text = PlainText(data=b"A very secret message")
        cipher_text = plain_text.encrypt(private_key, private_key.public_key())
        cipher_text2 = plain_text.encrypt(private_key, private_key.public_key())
        self.assertNotEqual(cipher_text, cipher_text2)

    def test_signature_valid(self):
        from council_decision.crypto.private_key import EllipticCurvePrivateKey
        from council_decision.crypto.plain_text import PlainText
        from council_decision.crypto.signature import Signature

        private_key = EllipticCurvePrivateKey()
        plain_text = PlainText(data=b"A very secret message")
        signature = private_key.sign(plain_text)
        self.assertIsInstance(signature, Signature)
        private_key.verify(signature, plain_text)

    def test_signature_invalid(self):
        from council_decision.crypto.private_key import EllipticCurvePrivateKey
        from council_decision.crypto.plain_text import PlainText
        from council_decision.crypto.signature import Signature
        from council_decision.crypto import InvalidSignature

        private_key = EllipticCurvePrivateKey()
        plain_text = PlainText(data=b"A very secret message")
        plain_text2 = PlainText(data=b"A veri secret message")
        signature = private_key.sign(plain_text)
        self.assertIsInstance(signature, Signature)
        with self.assertRaises(InvalidSignature):
            private_key.verify(signature, plain_text2)
