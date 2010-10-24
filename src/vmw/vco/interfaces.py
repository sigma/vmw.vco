from zope.interface import Interface

class ITypedValue(Interface):

    def type(self):
        """Return the type of the object (a string)."""

    def value(self):
        """Return the representation of the object value (a string)."""

# automatically register adapters from this module
import adapters
adapters = adapters
