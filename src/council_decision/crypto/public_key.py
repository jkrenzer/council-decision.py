from abc import ABC, abstractmethod
from typing import Any, Union
from pydantic import Field
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.hazmat.primitives.ciphers import Cipher
from cryptography.hazmat.primitives.hashes import Hash, SHA256
from cryptography.hazmat.primitives.padding import PKCS7
from council_decision.crypto.signature import Signable, Signature

from council_decision.pydantic import BaseModel, cryptography

from .signature import Signature, Signable


class PublicKey(BaseModel, ABC):
    key: Any
    private_key: Union[Any, None]

    @abstractmethod
    def encrypt_to(
        self, plain_text: "PlainText", own_private_key: Union["PrivateKey", None] = None
    ) -> "CipherText":
        pass

    @abstractmethod
    def verify(self, signature: Signature, data: Signable):
        pass

    def __eq__(self, __value: "PublicKey") -> bool:
        return self.key.public_numbers() == __value.key.public_numbers()


class EllipticCurvePublicKey(PublicKey):
    key: "cryptography.EllipticCurvePublicKey"
    private_key: Union["EllipticCurvePrivateKey", None] = None

    def encrypt_to(
        self,
        plain_text: "PlainText",
        own_private_key: Union["EllipticCurvePrivateKey", None] = None,
    ) -> "CipherText":
        own_private_key = (
            own_private_key if own_private_key is not None else self.private_key
        )
        if own_private_key is None:
            raise KeyError(
                "No own private key given for calculating shared communication key!"
            )
        shared_cipher: Cipher = own_private_key.shared_cipher(self)
        encryptor = shared_cipher.encryptor()
        data = plain_text.data
        padder = PKCS7(256).padder()
        padded_data = padder.update(data) + padder.finalize()
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        return CipherText(
            data=encrypted_data, info={"iv": shared_cipher.mode.initialization_vector}
        )

    def verify(self, signature: Signature, data: Signable, hash: Hash = SHA256) -> None:
        self.key.verify(signature.data, data.data, ec.ECDSA(hash()))


# class RsaPublicKey(PublicKey):
#     pass

AnyPublicKey = Union[EllipticCurvePublicKey]

from .private_key import PrivateKey, EllipticCurvePrivateKey
from .cipher_text import CipherText
from .plain_text import PlainText
