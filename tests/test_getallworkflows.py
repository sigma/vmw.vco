from mock_transports import TransportFactory
from base import TestCase
import sys

from vmw.vco.client import Client, Workflow

_fake_url = "http://vco.example.com/vmware-vmo-webcontrol/webservice"
_operation = "getAllWorkflows"

class TestGetAllWorkflows(TestCase):

    def setUp(self):
        self._transport = TransportFactory()
        self._client = Client(_fake_url,
                              username="foo", password="bar",
                              transport=self._transport)

    def _testWorkflowsBase(self, params):
        self._transport.recordTransaction(_operation,
                                          response_params = params)

        wfs = self._client.getAllWorkflows()
        self.assertTrue(isinstance(wfs, list))
        for wf in wfs:
            self.assertTrue(isinstance(wf, Workflow))
        return wfs

    def testNoWorkflow(self):
        _params = {'workflows': []}
        self._testWorkflowsBase(_params)

    def testMinimalWorkflow(self):
        _params = {'workflows': [{'name': "Plop"}]}
        self._testWorkflowsBase(_params)

    def testCompleteWorkflow(self):
        _params = {'workflows': [{'name': "Plop",
                                  'description': "dummy workflow",
                                  'id': "12345-67890",
                                  'input': [{'name': "in1",
                                             'type': "type1"}],
                                  'output': [{'name': "out1",
                                              'type': "type1"}],
                                  'attributes': [{'name': "attr1",
                                                  'type': "type1"}]}]}
        wfs = self._testWorkflowsBase(_params)
        self.assertEquals(len(wfs), 1)
