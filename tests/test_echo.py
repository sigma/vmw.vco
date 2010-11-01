from mock_transports import TransportFactory
from base import TestCase
from xml.sax.saxutils import escape as xml_escape

from vmw.vco.client import Client

_fake_url = "http://vco.example.com/vmware-vmo-webcontrol/webservice"
_echo_operation = "echo"

class TestEcho(TestCase):

    def setUp(self):
        self._transport = TransportFactory()
        self._client = Client(_fake_url,
                              transport=self._transport)

    def _testEchoBase(self, msg):
        self._transport.recordTransaction(_echo_operation,
                                          request_checker = lambda req: req._message == msg,
                                          response_params = {'message': xml_escape(msg)})

        resp = self._client.echo(msg)
        self.assertEqual(resp, msg)

    def testEcho(self):
        self._testEchoBase("plop")

    def testEchoEmpty(self):
        self._testEchoBase("")

    def testEchoLong(self):
        self._testEchoBase("repeated pattern"*50)

    def testEchoXml(self):
        self._testEchoBase("<foo/><bar>baz</bar>")
