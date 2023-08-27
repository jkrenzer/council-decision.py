from council_decision.pydantic import BaseModel

from .bytes import Bytes

Signable = Bytes

class Signature(Bytes):
    pass