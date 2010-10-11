from zope.interface import classImplements
from twisted.python import components
from interfaces import ITypedValue

def adapter(ifrom, ito):
    """Decorator to help registering a new adapter.

    :param ifrom: interface or class to adapt
    :param ito: interface to expose
    """
    def _adapter(cls):
        classImplements(cls, ito)
        components.registerAdapter(cls, ifrom, ito)
        return cls
    return _adapter

class PrimitiveAdapter(object):

    def __init__(self, original):
        self._original = original

    def value(self):
        return "%s" % (self._original)

@adapter(str, ITypedValue)
class StringValue(PrimitiveAdapter):
    """Adapter from string to ITypedValue."""

    def type(self):
        return "string"

@adapter(int, ITypedValue)
class IntValue(PrimitiveAdapter):
    """Adapter from int to ITypedValue."""

    def type(self):
        return "number"

@adapter(bool, ITypedValue)
class BoolValue(PrimitiveAdapter):
    """Adapter from bool to ITypedValue."""

    def type(self):
        return "boolean"
