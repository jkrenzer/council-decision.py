from Decision.Xml import Serializable, Settings
from Decision.Xml import Parser
from Decision.Xml.Validation import Constraint
from Decision.Xml.Validation import Validatable
from . import Vote

class Class(Serializable.Class, Validatable.Class):
    _tag = Settings.namespaceTag + "announcement"
    _validationScheme = {
        "@title": Constraint.Type(str) + Constraint.Count(maximum=1),
        "description": Constraint.Type(Serializable.Class) + Constraint.Count(maximum=1),
        "votes": Constraint.Type(Vote.Votes)
    }

Parser.lookup.register(Class)
