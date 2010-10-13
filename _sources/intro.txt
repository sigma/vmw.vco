==============
 Introduction
==============

This Python module aims at providing a complete control layer over vCO's
public interface.

This includes vCO WebService.

By using this module, one can (hopefully) obtain reasonable integration of vCO
in a Python environment, as well as a useful testing environment.

The use cases covered by vmw.vco and this documentation are:

* Communicate with a KL.next vCO using the :doc:`SOAP interface <soap>`.
* Provide a consistent API for synchronous and asynchronous applications
  (`Twisted <http://www.twistedmatric.com/>`_ is supported)
* Write tests targetting vCO.
* Provide enough information to extend vmw.vco in such a way that the above use
  cases remain consistent.

Installation
============

vmw.vco is best installed using official package::

  $ pip install vmw.vco

This will fetch vmw.vco and its dependencies from `Pypi <http://pypi.python.org>`_

Specificities
=============

These bindings are declined in 2 similar, yet different versions: a synchronous
and an asynchronous one.

The synchronous version is based on the standard :mod:`httplib` module, while
the asynchronous version is based on the `Twisted
<http://www.twistedmatrix.com>`_ framework.

The differences in behavior between those two approaches are blurred as much as
possible, so that the developer should feel at home in any case.  Bottom line,
every call that goes to the server returns object ``X`` in synchronous mode,
and a ``Deferred`` object that resolves to ``X`` in asynchronous mode.
