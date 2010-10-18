from mock_transports import TransportFactory
from unittest import TestCase

from vmw.vco.client import Client

_fake_url = "http://vco.example.com/vmware-vmo-webcontrol/webservice"
_echo_operation = "echo"
_echo_msg = "plop"

class TestEcho(TestCase):

    def setUp(self):
        self._transport = TransportFactory()
        self._client = Client(_fake_url,
                              transport=self._transport)

    def testEcho(self):
        self._transport.recordTransaction(_echo_operation,
                                          request_checker = lambda req: req._message == _echo_msg,
                                          response_params = {'message': _echo_msg})

        resp = self._client.echo(_echo_msg)
        self.assertEqual(resp, _echo_msg)
