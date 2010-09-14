import time

import generated.VSOWebControlService_client_sync as sync_client
import generated.VSOWebControlService_client_async as async_client
#from generated.VSOWebControlService_types import *

from types import WorkflowTokenAttribute as _WorkflowTokenAttribute, Workflow as _Workflow
from vmw.ZSI import EvaluateException

from twisted.internet.defer import Deferred
from twisted.internet import task, reactor

class TypeWrapper(object):
    """
    Base class for type wrappers
    """
    def __init__(self, typ, val):
        self.type = typ
        self.value = str(val)

class Client(object):
    """
    Implementation of a vCO webservice client.
    Calls implemented: 100%

    - echo
    - echoWorkflow
    - answerWorkflowInput
    - cancelWorkflow
    - executeWorkflow
    - find
    - findForId
    - findRelation
    - hasChildrenInRelation
    - getAllPlugins
    - getAllWorkflows
    - getWorkflowForId
    - getWorkflowsWithName
    - getWorkflowTokenForId
    - getWorkflowTokenResult
    - getWorkflowTokenStatus
    - simpleExecuteWorkflow
    - hasRights
    - sendCustomEvent
    """

    # see https://wiki.eng.vmware.com/BFG:JiDine/LDAPSetups for default
    # credentials
    def __init__(self,
                 url = "http://localhost:8280/vmware-vmo-webcontrol/webservice",
                 username = "admin",
                 password = "admin",
                 async = False,
                 **kw):
        self._url = url
        self._username = username
        self._password = password

        if async:
            self._mod = async_client
            self.service = async_client.VSOWebControlServiceLocator().getwebservice(url, **kw)
            self.service.binding.defer = async
        else:
            self._mod = sync_client
            self.service = sync_client.VSOWebControlServiceLocator().getwebservice(url, **kw)

        self._generateAccessor("getAllWorkflows",
                               self._getWorkflowsTrans, True)
        self._generateAccessor("getWorkflowForId",
                               self._getWorkflowTrans, True)
        self._generateAccessor("getWorkflowsWithName",
                               self._getWorkflowsTrans, True)
        self._generateAccessor("executeWorkflow",
                               self._executeWorkflowTrans, True)
        self._generateAccessor("simpleExecuteWorkflow",
                               self._executeWorkflowTrans, ('in1', 'in2'))
        self._generateAccessor("answerWorkflowInput",
                               None, True)
        self._generateAccessor("cancelWorkflow",
                               None, True)
        self._generateAccessor("getWorkflowTokenForId",
                               self._getWorkflowTokenForIdTrans, True)
        self._generateAccessor("getWorkflowTokenResult",
                               self._getWorkflowTokenResultTrans, True)
        self._generateAccessor("getWorkflowTokenStatus",
                               self._getWorkflowTokenStatusTrans, True)
        self._generateAccessor("getAllPlugins",
                               self._getAllPluginsTrans, True)
        self._generateAccessor("hasRights",
                               None, True)
        self._generateAccessor("sendCustomEvent",
                               None, True)
        self._generateAccessor("find",
                               self._findTrans, True)
        self._generateAccessor("findForId",
                               self._findForIdTrans, True)
        self._generateAccessor("findRelation",
                               self._findRelationTrans, True)
        self._generateAccessor("hasChildrenInRelation",
                               self._hasChildrenInRelationTrans, True)

        self._generateAccessor("echoWorkflow", self._getWorkflowTrans)
        self._generateAccessor("echo")

    def _isAsynchronous(self):
        return self._mod is async_client

    def getAllWorkflows(self):
        return self._getAllWorkflows()

    def getAllPlugins(self):
        return self._getAllPlugins()

    def getWorkflowForId(self, id):
        return self._getWorkflowForId(workflowId=id)

    def getWorkflowsWithName(self, name):
        return self._getWorkflowsWithName(workflowName=name)

    def cancelWorkflow(self, token):
        return self._cancelWorkflow(workflowTokenId=token.id)

    def __readInputs(self, inputs):
        real_inputs = []
        for k in inputs.keys():
            i = _WorkflowTokenAttribute()
            i._name = k
            wrap = self._typeWrapper(inputs[k])
            i._type = wrap.type
            i._value = wrap.value
            real_inputs.append(i)
        return real_inputs

    def executeWorkflow(self, wf, inputs={}):
        return self._executeWorkflow(workflowId=wf.id,
                                     workflowInputs=self.__readInputs(inputs))

    def simpleExecuteWorkflow(self, wf, encoded_input):
        return self._simpleExecuteWorkflow(in0=wf.id, in3=encoded_input)

    def getWorkflowTokenForId(self, token):
        return self._getWorkflowTokenForId(workflowTokenId=token.id)

    def getWorkflowTokenResult(self, token):
        return self._getWorkflowTokenResult(workflowTokenId=token.id)

    def getWorkflowTokenStatus(self, tokens):
        return self._getWorkflowTokenStatus(workflowTokenIds=[t.id for t in tokens])

    def answerWorkflowInput(self, token, inputs={}):
        return self._answerWorkflowInput(workflowTokenId=token.id,
                                         answerInputs=self.__readInputs(inputs))

    def hasRights(self, task, right):
        return self._hasRights(taskId=task.id, right=right)

    def sendCustomEvent(self, event, props):
        props = "\n".join(["%s=%s" % (str(key), str(val))
                           for (key, val) in props.items()])
        return self._sendCustomEvent(eventName=event, serializedProperties=props)

    def find(self, type, query=""):
        return self._find(type=type, query=query)

    def findForId(self, type, id):
        try:
            return self._findForId(type=type, id=id)
        except EvaluateException:
            return None

    def findRelation(self, type, id, relation):
        try:
            return self._findRelation(parentType=type, parentId=id,
                                      relationName=relation)
        except EvaluateException:
            return []

    def hasChildrenInRelation(self, type, id, relation):
        return self._hasChildrenInRelation(parentType=type, parentId=id,
                                           relationName=relation)

    def echo(self, msg):
        return self._echo(message=msg)

    def echoWorkflow(self, wf):
        return self._echoWorkflow(workflowMessage=wf._holder)

    def _getAllPluginsTrans(self, res):
        return [Plugin(self, w) for w in res]

    def _getWorkflowTrans(self, res):
        return Workflow(self, res)

    def _getWorkflowsTrans(self, res):
        return [Workflow(self, w) for w in res]

    def _executeWorkflowTrans(self, res):
        return WorkflowToken(self, res)

    def _getWorkflowTokenForIdTrans(self, res):
        return WorkflowToken(self, res)

    def _getWorkflowTokenResultTrans(self, res):
        return [WorkflowTokenAttribute(self, t) for t in res]

    def _getWorkflowTokenStatusTrans(self, res):
        translate = {"running": WorkflowToken.RUNNING,
                     "waiting": WorkflowToken.WAITING,
                     "waiting-signal": WorkflowToken.WAITING_SIGNAL,
                     "canceled": WorkflowToken.CANCELLED,
                     "completed": WorkflowToken.COMPLETED,
                     "failed": WorkflowToken.FAILED}
        return [translate[r] for r in res]

    def _findTrans(self, res):
        if res._elements is None:
            return []
        return [FinderResult(r) for r in res._elements._item]

    def _findForIdTrans(self, res):
        return FinderResult(res)

    def _findRelationTrans(self, res):
        return [FinderResult(r) for r in res]

    def _hasChildrenInRelationTrans(self, res):
        return (res > 0)

    # magic method for generating method calling generated stuff
    def _generateAccessor(self, name, trans = None, auth = False):
        # compute class of correct request type
        cls = eval("self._mod." + name + "Request")
        def _func(**keywords):
            req = cls()
            # authenticated methods need username/password
            if auth:
                if type(auth) is bool:
                    req._username = self._username
                    req._password = self._password
                else:
                    # some broken calls have cryptic names instead...
                    user_field, pwd_field = auth
                    setattr(req, '_' + user_field, self._username)
                    setattr(req, '_' + pwd_field, self._password)
            keys = keywords.keys()
            # build the request object with all specified components
            for kw in keys:
                setattr(req, "_" + kw, keywords[kw])

            # call the generated method, and get response
            resp = getattr(self.service, name)(req)

            def __extractRes(resp, name, trans):
                # extract relevant value from response object
                res = getattr(resp, "_" + name + "Return", None)
                # optionally transform result
                return (trans and trans(res)) or res

            if isinstance(resp, Deferred):
                resp.addCallback(__extractRes, name, trans)
                return resp
            else:
                return __extractRes(resp, name, trans)

        # add the method to this object
        setattr(self, "_" + name, _func)

    def _typeWrapper(self, value):
        if isinstance(value, TypeWrapper):
            return value
        else:
            # try to wrap builtin types
            assoc = {str: "string", int: "number", bool: "boolean"}
            for t in assoc.keys():
                if type(value) is t:
                    return TypeWrapper(assoc[t], value)
            raise Exception("Unable to wrap type %s" % (type(value)))

class Plugin(object):
    def __init__(self, server, holder):
        self.name = holder._moduleName
        self.description = holder._moduleDescription
        self._repr = holder._moduleDisplayName
        self.version = holder._moduleVersion

        self._server = server

    def __repr__(self):
        return self._repr

class Workflow(object):
    def __init__(self, server, holder):
        self.id = holder._id
        self.name = holder._name
        self.description = holder._description
        self.inParameters = holder._inParameters
        self.outParameters = holder._outParameters
        self.attributes = holder._attributes

        self._server = server
        self._holder = holder

    def execute(self, inputs={}):
        return self._server.executeWorkflow(self, inputs)

class WorkflowToken(object):
    # order matters (see method isFinished())
    RUNNING        = 0
    WAITING        = 1
    WAITING_SIGNAL = 2
    CANCELLED      = 3
    COMPLETED      = 4
    FAILED         = 5

    def __init__(self, server, holder):
        self.id = holder._id
        self.title = holder._title
        self.workflowId = holder._workflowId
        self.currentItemName = holder._currentItemName
        self.currentItemState = holder._currentItemState
        self.globalState = holder._globalState
        self.startDate = holder._startDate
        self.endDate = holder._endDate
        self.xmlContent = holder._xmlContent

        self._server = server

    def cancel(self):
        return self._server.cancelWorkflow(self)

    def getResult(self):
        return self._server.getWorkflowTokenResult(self)

    def getStatus(self):
        if self._server._isAsynchronous():
            d = self._server.getWorkflowTokenStatus([self])
            d.addCallback(lambda st: st[0])
            return d
        return self._server.getWorkflowTokenStatus([self])[0]

    def isFinished(self):
        if self._server._isAsynchronous():
            return self.getStatus().addCallback(lambda st: st >= self.CANCELLED)
        return self.getStatus() >= self.CANCELLED

    def isWaiting(self):
        waiting_states = [self.WAITING, self.WAITING_SIGNAL]
        if self._server._isAsynchronous():
            return self.getStatus().addCallback(lambda st: st in waiting_states)
        return self.getStatus() in waiting_states

    def __wait(self, pred, poll, target=None):
        _async = target is not None
        def __checkPred(res):
            if res:
                target.callback(self)
                return res
            else:
                task.deferLater(reactor, poll, self.__wait, pred, poll, target)
                return

        if _async:
            return pred().addCallback(__checkPred)
        else:
            while not pred():
                time.sleep(poll)
            return True

    def waitResult(self, poll=1):
        if self._server._isAsynchronous():
            d = Deferred()
            self.__wait(self.isFinished, poll, d)
            return d.addCallback(lambda _: self.getResult())
        else:
            self.__wait(self.isFinished, poll)
            return self.getResult()

    def waitQuestion(self, poll=1):
        if self._server._isAsynchronous():
            d = Deferred()
            self.__wait(self.isFinished, poll, d)
            return d.addCallback(lambda _: self)
        else:
            self.__wait(self.isFinished, poll)
            return self

    def answer(self, inputs):
        return self._server.answerWorkflowInput(self, inputs)

class WorkflowTokenAttribute(object):
    def __init__(self, server, holder):
        self.name = holder._name
        self.type = holder._type
        self.value = holder._value

        self._server = server
        self._holder = holder

    def __repr__(self):
        return "<[%s:%s] %s>" % (self.name, self.type, self.value)

class Rights(object):
    READ = ord('r')
    WRITE = ord('c')
    EXECUTE = ord('x')

class FinderResult(object):
    def __init__(self, holder):
        self.type = holder._type
        self.id = holder._id
        self.uri = holder._dunesUri
        self.properties = self.__readProperties(holder._properties)

        self._holder = holder

    def __readProperties(self, props):
        res = {}
        for i in props._item:
            res[i._name] = i._value
        return res
