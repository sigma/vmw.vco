.. _examples:

===================
 SOAP client usage
===================

In these examples, an online `vCO simulator <http://vco-gae.appspot.com>`_, by
the same author, is used, so that examples should be runnable without any
modification, and without requiring installation of a vCO server.

In order to run the following examples against your own vCO server, connect the
``Client`` object to a URL like
http://<VCO_IP>:8280/vmware-vmo-webcontrol/webservice instead (8280 is the
default port used by vCO SOAP service).

Check the server connection
===========================

This simple example validates that everything is properly configured, by using
the ``echo``  test method of the vCO SOAP service::

  >>> from vmw.vco.client import Client

  >>> c = Client(url='http://vco-gae.appspot.com:80/vmware-vmo-webcontrol/webservice',
  ...            username='admin', password='admin')

  >>> print c.echo('foo')
  foo

Get list of available workflows
===============================

  >>> wfs = c.getAllWorkflows()

  >>> print wfs
  [<vmw.vco.client.Workflow object at 0x2ba0a10>, <vmw.vco.client.Workflow object at 0x2ba0cd0>]

  >>> for wf in wfs:
  ...     print wf.name
  ...
  Dummy workflow
  Waiting workflow

Run a workflow
==============

  >>> wf = wfs[0]

  >>> for i in wf.inParameters:
  ...     print "%s: %s" % (i.name, i.type)
  ...
  in: string

  >>> inputs = {'in': 'foo'}

  >>> run = wf.execute(inputs)

  >>> print run
  <vmw.vco.client.WorkflowToken object at 0x2bb2210>

Wait for a result
=================

  >>> run.waitResult()
  [<[out:string] foo>]
