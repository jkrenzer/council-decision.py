from Ballotage.Xml import Serializable, Settings
from .Xml import Parser
from .Xml.Validation import Constraint
from .Xml.Validation import Validatable
from . import Vote

class Class(Serializable.Class, Validatable.Class):
    _tag = Settings.namespaceTag + "announcement"
    _validationScheme = {
        "@title": Constraint.Type(str) + Constraint.Count(maximum=1),
        "description": Constraint.Type(Serializable.Class) + Constraint.Count(maximum=1),
        "votes": Constraint.Type(Vote.Votes)
    }

Parser.lookup.register(Class)
