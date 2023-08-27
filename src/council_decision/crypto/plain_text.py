from council_decision.pydantic import BaseModel

from .bytes import Bytes

class PlainText(Bytes):
    data: bytes

    def encrypt(self, key, own_private_key = None) -> 'CipherText':
        return key.encrypt(self, own_private_key)

from .cipher_text import CipherText