# Copyright (c) 2009-2010 VMware, Inc. All Rights Reserved.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

from zope.interface import classImplements
import vmw.vco.components as components
from vmw.vco.interfaces import ITypedValue

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

class StringValue(PrimitiveAdapter):
    """Adapter from string to ITypedValue."""

    def type(self):
        return "string"
StringValue = adapter(str, ITypedValue)(StringValue)

class IntValue(PrimitiveAdapter):
    """Adapter from int to ITypedValue."""

    def type(self):
        return "number"
IntValue = adapter(int, ITypedValue)(IntValue)

class BoolValue(PrimitiveAdapter):
    """Adapter from bool to ITypedValue."""

    def type(self):
        return "boolean"
BoolValue = adapter(bool, ITypedValue)(BoolValue)
