import os
from httplib import HTTPConnection
from jinja2 import Environment, FileSystemLoader

from vmw.vco.generated.VSOWebControlService_types import *
from vmw.ZSI.parse import ParsedSoap

class OperationResponse(object):

    tpl_env = Environment(loader=FileSystemLoader(os.path.dirname(__file__) + '/xml/responses'))

    def __init__(self, op):
        self.__tpl = self.tpl_env.get_template(op + ".xml")

    def render(self, **kwargs):
        content = self.__tpl.render(kwargs)
        return content

class HTTPResponse(object):

    def __init__(self, data):
        self.status = 200
        self.reason = 'OK'
        self.msg = HTTPMessage({'Content-Type': 'text/xml; charset="UTF-8"',
                                'Transfer-Encoding': 'chunked'})
        self._data = data

    def read(self):
        return self._data

class HTTPMessage(object):
    def __init__(self, headers):
        self.__headers = headers
        self.type = "text/xml"

    def getallmatchingheaders(self, name):
        return self.__headers.get(name, [])

def TransportFactory():

    class Transport(HTTPConnection):

        transactions = []
        index = 0

        @classmethod
        def recordTransaction(cls, operation, request_checker=None, response_params={}):
            if request_checker is None:
                request_checker = lambda _: True
            cls.transactions.append((operation, request_checker, response_params))

        def __init__(self, *args, **kwargs):
            HTTPConnection.__init__(self, *args, **kwargs)
            self.__getTransaction()

        def __getTransaction(self):
            try:
                self.__op, self.__check, self.__resp = self.transactions[self.index]
                self.__class__.index += 1
            except IndexError:
                pass

        def connect(self):
            pass

        def putheader(self, key, value):
            pass

        def putrequest(self, method, uri):
            assert method == "POST", "Wrong method '%s'" % (method)
            assert uri == "/vmware-vmo-webcontrol/webservice", "Wrong uri '%s'" % (uri)

        def endheaders(self):
            pass

        def send(self, data):
            ps = ParsedSoap(data)
            req = ps.Parse(GED(ns0.targetNamespace, self.__op))
            assert self.__check(req)

        def getresponse(self):
            data = OperationResponse(self.__op).render(**(self.__resp))
            return HTTPResponse(data)

    return Transport
