from pydantic import Field
from council_decision.pydantic import BaseModel
from typing import Dict, Any

from .bytes import Bytes

class CipherText(Bytes):
    data: bytes
    info: Dict[str, Any] = Field(default_factory=dict)


    def decrypt(self, key) -> 'PlainText':
        return key.decrypt(self)

from .plain_text import PlainText