from lxml import etree
from . import Serializable

#Default lookup for fallback

fallbackLookup = etree.ElementDefaultClassLookup(element=Serializable.Class)

class _Lookup(etree.CustomElementClassLookup):

    def __init__(self):
        super(etree.CustomElementClassLookup,self).__init__(fallbackLookup)
        self._registry = {}


    def lookup(self, nodeType, document, namespace, name):
        nodeName = name
        if namespace is not None:
            nodeName = ("{%s}" % namespace) + name
        if nodeType == "element" and nodeName in self._registry.keys():
            print(nodeName)
            return self._registry.get(nodeName, None)
        else:
            return None #Fallback to default

    def register(self, cls):
        self._registry.update({
            str(cls._tag): cls
        })


parser = etree.XMLParser()
lookup = _Lookup()
parser.set_element_class_lookup(lookup)
