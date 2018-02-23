from lxml import etree
import uuid
import pprint as pp
import copy
from . import Validation
from Ballotage import HelperFunctions

class Class(etree.ElementBase):
    
    _tag = None

    def _init(self):
        super(etree.ElementBase, self)._init()
        if self._tag is not None:
            self.tag = copy.copy(self._tag)

    def getChildren(self, name, default=None, namespaces=None, cast=None):
        children = self.findall(path=name, namespaces=namespaces)
        if cast is None:
            return children
        else:
            transformedChildren = [_transform(child,default=default,cast=cast) for child in children]
            return transformedChildren

    def getAttribute(self, name, default=None, cast=None):
        if name[0] == "@":
            name = name[1:] #Stripping leftover attribute signifiers
        if cast is None:
            return super(etree.ElementBase,self).get(name,default)
        else:
            stringValue = super(etree.ElementBase,self).get(name, None)
            if stringValue is None:
                return default
            else:
                try:
                    value = cast(super(etree.ElementBase,self).get(name))
                except ValueError:
                    value = default
                return value

    def getAll(self, name, default=None, cast=None, namespaces=None):
        if name[:1] == "@":
            name = name[1:]
            return [self.getAttribute(name=name,default=default,cast=cast)]
        else:
            return self.getChildren(name=name,default=default,namespaces=namespaces,cast=cast)

    def get(self, name, default=None, cast=None, namespaces=None):
        return next(iter((self.getAll(name=name,default=default,cast=cast,namespaces=namespaces)) or []), default)

    def set(self, name, value):
        if name[:1] == "@":
            name = name[1:]
            super(etree.ElementBase,self).set(name,value)
        elif name is None:
            super(etree.ElementBase,self).append(value)
        else:
            value.tag = name
            super(etree.ElementBase,self).append(value)
