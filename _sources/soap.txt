=========================
 Developer documentation
=========================

SOAP interface
==============

Main entry point
----------------

The main entry point is:

.. autoclass:: vmw.vco.client.Client()
   :members:

   .. automethod:: vmw.vco.client.Client.__init__(self, url, username, password, async=False, **kw)

Helper objects
--------------

A collection of helpers is also provided, that make use of the API more object-oriented:

.. autoclass:: vmw.vco.client.Plugin()
   :members:

.. autoclass:: vmw.vco.client.Workflow()
   :members:

.. autoclass:: vmw.vco.client.WorkflowAttribute()
   :members:

.. autoclass:: vmw.vco.client.WorkflowToken()
   :members:

.. autoclass:: vmw.vco.client.FinderResult()
   :members:

Using objects
=============

A surprisingly challenging part in using vCO SOAP API is to provide workflows
with proper input parameters. For that it's necessary to generate valid
representations of all types that can be used as input. For immediate values,
it's rather easy (and worst case, :class:`vmw.vco.client.TypedValue` can be
used to wrap anything).

.. autoclass:: vmw.vco.client.TypedValue()
   :members:

   .. automethod:: vmw.vco.client.TypedValue.__init__(self, type, value)

For objects, it's more complicated, as they can come from different places
(workflow output, finder result, other component that's specific to your
application's logic).

The rule in vmw.vco is that a valid input is something that implements the
interface :class:`vmw.vco.interfaces.ITypedValue`. This include of
course :class:`vmw.vco.components.TypedValue`, but also everything that has an
*adapter* registered for that interface.

In particular, the *adapters* from :mod:`vmw.vco.adapters` are loaded by default.

.. automodule:: vmw.vco.adapters
   :members:

So, if you have some custom objects that could be transformed into an input
value, just register an adapter for it, and pass it !
