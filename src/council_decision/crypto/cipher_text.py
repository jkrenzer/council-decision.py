from pydantic import Field
from council_decision.pydantic import BaseModel
from typing import Dict, Any, Union

from .bytes import Bytes


class CipherText(Bytes):
    data: bytes
    info: Dict[str, Any] = Field(default_factory=dict)

    def decrypt(
        self,
        key: Union["PublicKey", "PrivateKey"],
        other_key: Union["PrivateKey", "PublicKey"],
    ) -> "PlainText":
        return key.decrypt_from(self, other_key)


from .plain_text import PlainText
from .private_key import PrivateKey
from .public_key import PublicKey
