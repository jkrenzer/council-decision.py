from . import Serializable
from .Validation import Constraint
import math

class Class(Serializable.Class):

    def _init(self,cls,minimum=1,maximum=math.inf):
        self._childType = cls
        self._validationScheme = {
            cls._tag: Constraint.Type(cls) + Constraint.Count(minimum=minimum,maximum=maximum)
        }
        if self._tag is None:
            self._tag = cls._tag + "s"
        super(Serializable.Class, self)._init()
