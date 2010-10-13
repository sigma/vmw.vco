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

Synchronous examples
====================

Check the server connection
---------------------------

This simple example validates that everything is properly configured, by using
the ``echo``  test method of the vCO SOAP service::

  >>> from vmw.vco.client import Client

  >>> c = Client(url='http://vco-gae.appspot.com:80/vmware-vmo-webcontrol/webservice',
  ...            username='admin', password='admin')

  >>> print c.echo('foo')
  foo

Get list of available workflows
-------------------------------

Now let's see what workflows are available in that vCO server::

  >>> wfs = c.getAllWorkflows()

  >>> print wfs
  [<vmw.vco.client.Workflow object at 0x2ba0a10>, <vmw.vco.client.Workflow object at 0x2ba0cd0>]

  >>> for wf in wfs:
  ...     print wf.name
  ...
  Dummy workflow
  Waiting workflow

Sanity-check the client
-----------------------

Similar to the ``echo`` command, there is an ``echoWorkflow`` one, that
requires the client to provide some well-formatted workflow object::

  >>> wf = wfs[0]

  >>> print c.echoWorkflow(wf)
  <vmw.vco.client.Workflow object at 0x36d2650>

Run a workflow
--------------

Select a workflow, discover the inputs it requires, and run it::

  >>> for i in wf.inParameters:
  ...     print "%s: %s" % (i.name, i.type)
  ...
  in: string

  >>> inputs = {'in': 'foo'}

  >>> run = wf.execute(inputs)

  >>> print run
  <vmw.vco.client.WorkflowToken object at 0x2bb2210>

Wait for a result
-----------------

Wait for workflow completion, and retrieve output::

  >>> res = run.waitResult()
  {'out': <vmw.vco.components.TypedValue object at 0x1b7a690>}

  >>> print res['out'].value()
  foo

Cancel a workflow
-----------------

If some workflow has been run by mistake, you can always cancel it. That will
not undo what's already done, but will attempt to prevent from going further::

  >>> run = wf.execute(inputs)

  >>> run.cancel()

Answer a workflow interaction
-----------------------------

Some workflows require additional inputs in the middle of their execution,
requiring more interactions::

  >>> wf = wfs[1]

  >>> run = wf.execute()

  >>> run.waitQuestion()

  >>> run.answer({'answer': 42})

  >>> run.waitResult()
  {}

Asynchronous examples
=====================

Here is a quick scenario to demonstrate how to use this API in an asynchronous
way::

  from vmw.vco.client import Client
  from twisted.internet import reactor

  def dummy():
      c = Client(url='http://vco-gae.appspot.com:80/vmware-vmo-webcontrol/webservice',
                 username='admin', password='admin', async=True)

      def _display(val):
          print val

      c.getWorkflowForId("94db6b5e-cabf-11df-9ffb-002618405f6e")\
       .addCallback(lambda wf: wf.execute({'in': 'foo'}))\
       .addCallback(lambda run: run.WaitResult())\
       .addCallback(lambda res: _display(res[out]))

  dummy()
  reactor.run()


Alternately, using a Monocle-like syntax::

  from vmw.vco.client import Client
  from twisted.internet import reactor
  from twisted.internet.defer import inlineCallbacks as _o

  @_o
  def dummy():
      c = Client(url='http://vco-gae.appspot.com:80/vmware-vmo-webcontrol/webservice',
                 username='admin', password='admin', async=True)

      wf = yield c.getWorkflowForId("94db6b5e-cabf-11df-9ffb-002618405f6e")
      run = yield wf.execute({'in': 'foo'})
      res = yield run.WaitResult()
      print res[out]

  dummy()
  reactor.run()
