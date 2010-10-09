.. _examples:

===================
 SOAP client usage
===================

In these examples, an online vCO simulator is used, so that examples should be
runnable without any modification, and without requiring installation of
a vCO server.

Check the server connection
===========================

This simple example validates that everything is properly configured, by using
the ``echo``  test method of the vCO SOAP service::

  from vmw.vco.client import Client

  c = Client(url='http://vco-gae.appspot.com:80/vmware-vmo-webcontrol/webservice',
             username='admin', password='admin')
  print c.echo('foo')

This should obviously print ''foo'' in return.
