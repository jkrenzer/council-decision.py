import types
import math
from Ballotage.HelperFunctions import _transform

class Class:

    def validate(self):
        results = {
            None: True
        }
        for field, constraint in self.validationScheme.items():
            values = self.getAll(name=field, default=None)
            results.update({field: constraint.evaluate(values)})
        return results

    def validated(instance):
        if instance.isValid():
            return instance
        else:
            return None

    def isValid(self):
        results = self.validate()
        if all(results.values()):
            return True
        else:
            return False
