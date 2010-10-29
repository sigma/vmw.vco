import sys
from mock_transports import TransportFactory
from unittest import TestCase
from nose.plugins.attrib import attr

from vmw.vco.client import Client, Plugin

_fake_url = "http://vco.example.com/vmware-vmo-webcontrol/webservice"
_operation = "getAllPlugins"

class TestGetAllPlugins(TestCase):

    def setUp(self):
        self._transport = TransportFactory()
        self._client = Client(_fake_url,
                              username="foo", password="bar",
                              transport=self._transport)

    def _testPluginBase(self, params):
        self._transport.recordTransaction(_operation,
                                          response_params = params)

        plugs = self._client.getAllPlugins()
        self.assertTrue(isinstance(plugs, list))
        for p in plugs:
            self.assertTrue(isinstance(p, Plugin))

    @attr(state="stable")
    def testBasicPlugin(self):
        _params = {'plugins': [{'name': 'plop',
                                'version': '0.1',
                                'desc': 'plop plug-in',
                                'display': 'Plop'}]}
        self._testPluginBase(_params)

    @attr(state="stable")
    def testIncompletePlugins(self):
        _params = {'plugins': [{'version': '0.1',
                                'desc': 'plop plug-in',
                                'display': 'Plop'},
                               {'name': 'plop',
                                'desc': 'plop plug-in',
                                'display': 'Plop'},
                               {'name': 'plop',
                                'version': '0.1',
                                'display': 'Plop'},
                               {'name': 'plop',
                                'version': '0.1',
                                'desc': 'plop plug-in'}]}
        self._testPluginBase(_params)
