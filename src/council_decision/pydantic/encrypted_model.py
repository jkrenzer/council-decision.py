from typing import Tuple, Type
from pydantic import UUID4

from council_decision.identity.identity import Identity
from council_decision.crypto.cipher_text import CipherText
from council_decision.encryption_context import Encryption
from .base_model import BaseModel


class Encrypted(BaseModel):
    cipher_text: CipherText
    participants: Tuple[UUID4, UUID4]
    _type: None

    def __class_getitem__(cls, wrapped_type: Type):
        return type(
            "Encrypted__" + wrapped_type.__name__, (Encrypted,), {"_type": wrapped_type}
        )

    @classmethod
    def original_type(cls):
        return cls._type
