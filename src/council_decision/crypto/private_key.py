import os
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Union, Literal, Annotated, Type
from pydantic import Field
from cryptography.hazmat.primitives.asymmetric import ec, rsa
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.kdf.concatkdf import ConcatKDFHash
from cryptography.hazmat.primitives.ciphers import (
    Cipher,
    algorithms,
    modes,
    BlockCipherAlgorithm,
)
from cryptography.hazmat.primitives.padding import PKCS7
from cryptography.hazmat.primitives.hashes import Hash, SHA256


from council_decision.pydantic import BaseModel

from .signature import Signature, Signable
from .dump_password import DumpPassword


class BasePrivateKey(BaseModel, ABC):
    key: Any

    class KeyType(Enum):
        EC = "EC"
        RSA = "RSA"

    type: KeyType

    @classmethod
    def create(cls, type: KeyType = KeyType.EC) -> "PrivateKey":
        key_type_map = {
            cls.KeyType.EC: EllipticCurvePrivateKey,
        }
        return key_type_map.get(type, EllipticCurvePrivateKey)()

    @abstractmethod
    def decrypt_from(
        self,
        cipher_text: "CipherText",
        peer_public_key: Union["PublicKey", None] = None,
    ) -> "PlainText":
        pass

    @abstractmethod
    def sign(self, data: Signable) -> Signature:
        pass

    @abstractmethod
    def public_key(self) -> "PublicKey":
        pass

    def verify(self, signature: Signature, data: Signable):
        return self.public_key().verify(signature, data)

    def encrypt_to(
        self, plain_text: "PlainText", peer_public_key: "PublicKey" = None
    ) -> "CipherText":
        if peer_public_key is None:
            peer_public_key = self.key.public_key()
        return peer_public_key.encrypt_to(plain_text, self)

    def __eq__(self, __value: "PrivateKey") -> bool:
        return self.key.private_numbers() == __value.key.private_numbers()

    def lock(self, password: Union[bytes, None] = None) -> "LockedPrivateKey":
        if password is None:
            password = DumpPassword.get()
        return LockedPrivateKey(
            locked_key=self.key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(password),
            ),
            unlocked_type=type(self),
        )


class LockedPrivateKey(BaseModel):
    locked_key: bytes
    unlocked_type: Type

    def unlock(self, password: Union[bytes, None] = None) -> "PrivateKey":
        if password is None:
            password = DumpPassword.get()
        return self.unlocked_type(
            key=serialization.load_pem_private_key(self.locked_key, password)
        )


class EllipticCurvePrivateKey(BasePrivateKey):
    key: "cryptography.EllipticCurvePrivateKey" = Field(
        default_factory=lambda: ec.generate_private_key(ec.SECP384R1())
    )
    type: Literal[BasePrivateKey.KeyType.EC] = BasePrivateKey.KeyType.EC

    def shared_cipher(
        self,
        peer_public_key: "EllipticCurvePublicKey",
        algorithm: BlockCipherAlgorithm = algorithms.AES,
        mode: modes.Mode = modes.CBC,
        mode_parameters=None,
    ) -> Cipher:
        if mode_parameters is None and mode is modes.CBC:
            mode_parameters = [os.urandom(16)]
        exchange_key = self.key.exchange(
            algorithm=ec.ECDH(), peer_public_key=peer_public_key.key
        )
        key_derivation_function = ConcatKDFHash(
            algorithm=hashes.SHA256(),
            length=32,
            otherinfo=bytes(__name__, encoding="UTF-8"),
        )
        return Cipher(
            algorithm=algorithm(key_derivation_function.derive(exchange_key)),
            mode=mode(*mode_parameters),
        )

    def public_key(self) -> "EllipticCurvePublicKey":
        return EllipticCurvePublicKey(key=self.key.public_key(), private_key=self)

    def decrypt_from(
        self,
        cipher_text: "CipherText",
        peer_public_key: Union["EllipticCurvePublicKey", None] = None,
    ) -> "PlainText":
        peer_public_key = (
            peer_public_key if peer_public_key is not None else self.public_key()
        )
        if peer_public_key is None:
            raise KeyError("No peer public key given to calculate shared cipher!")
        decryptor = self.shared_cipher(
            peer_public_key, mode_parameters=[cipher_text.info["iv"]]
        ).decryptor()
        padded_data = decryptor.update(cipher_text.data) + decryptor.finalize()
        unpadder = PKCS7(256).unpadder()
        data = unpadder.update(padded_data) + unpadder.finalize()
        return PlainText(data=data)

    def sign(self, data: Signable, hash: Hash = SHA256) -> Signature:
        return Signature(data=self.key.sign(data.data, ec.ECDSA(hash())))


# class RsaPrivateKey(PrivateKey):
#     key: rsa.RSAPrivateKey

#     def decrypt(self, cipher_text: CipherText, peer_public_key) -> PlainText:
#         return super().decrypt(data, peer_public_key)

#     def sign(self, data: Signable) -> Signature:
#         return super().sign(data)

PrivateKey = BasePrivateKey

AnyPrivateKey = Union[EllipticCurvePrivateKey]

from council_decision.pydantic import cryptography
from .public_key import PublicKey, EllipticCurvePublicKey
from .plain_text import PlainText
from .cipher_text import CipherText
