from pydantic import Field
from council_decision.pydantic import BaseModel

from .private_key import PrivateKey, AnyPrivateKey
from .public_key import PublicKey
from .cipher_text import CipherText
from .plain_text import PlainText
from .signature import Signature, Signable


class KeyRing(BaseModel):
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
