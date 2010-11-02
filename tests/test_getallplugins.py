from mock_transports import TransportFactory
from base import TestCase
import sys

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
        return plugs

    def testBasicPlugin(self):
        _params = {'plugins': [{'name': 'plop',
                                'version': '0.1',
                                'desc': 'plop plug-in',
                                'display': 'Plop'}]}
        self._testPluginBase(_params)

    def testEmptyPlugin(self):
        _params = {'plugins': [{}]}
        self._testPluginBase(_params)

    def testNoPlugin(self):
        _params = {}
        self._testPluginBase(_params)

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
