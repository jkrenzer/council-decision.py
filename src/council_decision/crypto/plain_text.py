from typing import Union
from council_decision.pydantic import BaseModel

from .bytes import Bytes


class PlainText(Bytes):
    data: bytes

    def encrypt(
        self,
        key: Union["PublicKey", "PrivateKey"],
        other_key: Union["PrivateKey", "PublicKey"],
    ) -> "CipherText":
        if isinstance(key, PublicKey):
            assert isinstance(
                other_key, PrivateKey
            ), "You have to give one private and one public key!"
        if isinstance(key, PrivateKey):
            assert isinstance(
                other_key, PublicKey
            ), "You have to give one private and one public key!"
        return key.encrypt_to(self, other_key)


from .cipher_text import CipherText
from .private_key import PrivateKey
from .public_key import PublicKey
