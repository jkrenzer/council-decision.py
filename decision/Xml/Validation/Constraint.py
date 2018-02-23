import types
import math
import pprint as pp

class ConstraintBase:
    # def __init__(self):
    #     self._constraints = {}

    def __add__(self, other):
        if not hasattr(self,'_constraints'):
            self._constraints = []
        if isinstance(other, ConstraintBase) and other not in self._constraints:
            self._constraints.append(other)
            return self

    def evaluate(self, objectList):
        if hasattr(self, "_constraints"):
            for constraint in self._constraints:
                if constraint._evaluate(objectList) is False:
                    print("Constraint %s failed!" % type(constraint))
                    return False
        return self._evaluate(objectList)

class Type(ConstraintBase):
    def __init__(self, requiredType):
        self.requiredType = requiredType

    def _evaluate(self, objectList):
        for obj in objectList:
            print(type(obj))
            if type(obj) is not self.requiredType:
                try:
                    self.requiredType(obj)
                except:
                    return False
        return True

class Count(ConstraintBase):
    def __init__(self,minimum=1,maximum=math.inf):
        if minimum >= 1:
            self.minimum = minimum
        else:
            self.minimum = 1
        if maximum >= minimum:
            self.maximum = maximum
        else:
            self.maximum = minimum

    def _evaluate(self, objectList):
        if self.minimum is not None and len(objectList) < self.minimum:
            return False
        elif self.maximum is not None and len(objectList) > self.maximum:
            return False
        else:
            return True

class Function(ConstraintBase):
    def __init__(self,func):
        self.func = func

    def _evaluate(self,objectList):
        for obj in objectList:
            if self.func(obj) is False:
                return False
        return True
