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

    def _compareWorkflow(self, wf, wf_def):
        self.assertEquals(wf_def['name'], wf.name)
        self.assertEquals(wf_def['description'], wf.description)
        self.assertEquals(wf_def['id'], wf.id)

    def testNoWorkflow(self):
        _params = {'workflows': []}
        self._testWorkflowsBase(_params)

    def testMinimalWorkflow(self):
        _params = {'workflows': [{'name': "Plop"}]}
        wfs = self._testWorkflowsBase(_params)
        self.assertEquals(len(wfs), 1)
        self.assertEquals(wfs[0].name, "Plop")

    def testCompleteWorkflow(self):
        wf0 = {'name': "Plop",
               'description': "dummy workflow",
               'id': "12345-67890",
               'input': [{'name': "in1", 'type': "type1"}],
               'output': [{'name': "out1", 'type': "type1"}],
               'attributes': [{'name': "attr1", 'type': "type1"}]}
        _params = {'workflows': [wf0]}
        wfs = self._testWorkflowsBase(_params)
        self.assertEquals(len(wfs), 1)
        self._compareWorkflow(wfs[0], wf0)
