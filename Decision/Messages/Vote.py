from .Xml import Serializable
from .Xml import Collection
from .Xml import Settings
from .Xml.Validation import Constraint

class Votes(Collection.Class):
    pass

class Class(Serializable.Class):
    _tag = Settings.namespaceTag + "vote"
    _classValidationScheme = {
        "@title": Constraint.Type(str) + Constraint.Count(maximum=1),
        "description": Constraint.Type(Serializable.Class) + Constraint.Count(maximum=1),
    }
