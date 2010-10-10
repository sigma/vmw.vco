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
* Write tests targetting vCO.
* Provide enough information to extend vmw.vco in such a way that the above use
  cases remain consistent.

Installation
============

vmw.vco is best installed using official package::

  $ pip install vmw.vco

This will fetch vmw.vco and its dependencies from `Pypi <http://pypi.python.org>`_
