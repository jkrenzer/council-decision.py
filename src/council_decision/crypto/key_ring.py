from typing import Union
from pydantic import Field
from council_decision.pydantic import BaseModel

from .private_key import PrivateKey, LockedPrivateKey, AnyPrivateKey
from .public_key import PublicKey, AnyPublicKey
from .cipher_text import CipherText
from .plain_text import PlainText
from .signature import Signature, Signable


class PublicKeyRing(BaseModel):
    private_key_ring: Union["PrivateKeyRing", None] = None
    encryption_public_key: AnyPublicKey
    signature_public_key: AnyPublicKey

    def encrypt_to(
        self, plain_text: PlainText, own_private_key: PrivateKey
    ) -> CipherText:
        return self.encryption_public_key.encrypt_to(plain_text, own_private_key)

    def verify(self, signature: Signature, signabe_obj: Signable) -> None:
        self.signature_public_key.verify(signature, signabe_obj)


class PrivateKeyRing(BaseModel):
    encrpytion_private_key: AnyPrivateKey = Field(default_factory=PrivateKey.create)
    signature_private_key: AnyPrivateKey = Field(default_factory=PrivateKey.create)

    def encrypt_to(
        self, plain_text: PlainText, peer_public_key: PublicKey
    ) -> CipherText:
        return self.encrpytion_private_key.encrypt_to(plain_text, peer_public_key)

    def encrypt(self, plain_text: PlainText) -> CipherText:
        return self.encrypt_to(plain_text, self.encrpytion_private_key.public_key())

    def decrypt_from(
        self, cipher_text: CipherText, peer_pblic_key: PublicKey
    ) -> PlainText:
        return self.encrpytion_private_key.decrypt_from(cipher_text, peer_pblic_key)

    def decrypt(self, cipher_text: CipherText) -> PlainText:
        return self.decrypt_from(cipher_text, self.encrpytion_private_key.public_key())

    def sign(self, signable_obj: Signable) -> Signature:
        return self.signature_private_key.sign(signable_obj)

    def verify(self, signature: Signature, signabe_obj: Signable) -> None:
        self.signature_private_key.verify(signature, signabe_obj)

    def public_key_ring(self):
        return PublicKeyRing(
            private_key_ring=self,
            encryption_public_key=self.encrpytion_private_key.public_key(),
            signature_public_key=self.signature_private_key.public_key(),
        )

    def lock(self, password: Union[bytes, None] = None):
        return LockedPrivateKeyRing(
            locked_encryption_key=self.encrpytion_private_key.lock(password),
            locked_signature_key=self.signature_private_key.lock(password),
        )


class LockedPrivateKeyRing(BaseModel):
    locked_encryption_key: LockedPrivateKey
    locked_signature_key: LockedPrivateKey

    def unlock(self, password: Union[bytes, None] = None):
        return PrivateKeyRing(
            encrpytion_private_key=self.locked_encryption_key.unlock(password),
            signature_private_key=self.locked_signature_key.unlock(password),
        )
