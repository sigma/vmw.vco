# Copyright (c) 2009-2010 VMware, Inc. All Rights Reserved.

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import time

import vmw.vco.generated.VSOWebControlService_client_sync as sync_client

from vmw.vco.types import WorkflowTokenAttribute as _WorkflowTokenAttribute
from vmw.ZSI import EvaluateException
from vmw.vco.interfaces import ITypedValue

# Twisted is optional
try:
    import vmw.vco.generated.VSOWebControlService_client_async as async_client
    from twisted.internet.defer import Deferred
    from twisted.internet import task, reactor
except ImportError:
    TWISTED_PRESENT = False
else:
    TWISTED_PRESENT = True

from zope.interface import implements

class Client(object):
    """
    Implementation of a vCO webservice client.
    API Calls implemented:

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

    def __init__(self,
                 url = "http://localhost:8280/vmware-vmo-webcontrol/webservice",
                 username = "admin",
                 password = "admin",
                 async = False,
                 **kw):
        """
        Build a client for target vCO server.

        :param url: full URL for the target vCO SOAP service
        :type url: string
        :param username: user name
        :type username: string
        :param password: password for the user
        :type password: string
        :param async: whether to use asynchronous bindings
        :type async: bool
        :param kw: keyword arguments passed to underlying ``Binding`` object
        :type kw: dict
        """
        self._url = url
        self._username = username
        self._password = password

        if async:
            assert TWISTED_PRESENT, "asynchronous mode cannot be used without Twisted library"
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
        """Retrieve all workflows installed in the server.

        :rtype: list of :class:`vmw.vco.client.Workflow`
        """
        return self._getAllWorkflows()

    def getAllPlugins(self):
        """Retrieve all plugins installed in the server.

        :rtype: list of :class:`vmw.vco.client.Plugin`
        """
        return self._getAllPlugins()

    def getWorkflowForId(self, id):
        """Retrieve workflow with specified id.

        :param id: Workflow id
        :type id: string
        """
        return self._getWorkflowForId(workflowId=id)

    def getWorkflowsWithName(self, name):
        """Retrieve all workflows with specified name (might be in different categories).

        :param name: Workflow name
        :type name: string
        """
        return self._getWorkflowsWithName(workflowName=name)

    def cancelWorkflow(self, token):
        """Cancel specified workflow token.

        :param token: Token to cancel
        :type token: vmw.vco.client.WorkflowToken
        """
        return self._cancelWorkflow(workflowTokenId=token.id)

    def __readInputs(self, inputs):
        real_inputs = []
        for k in list(inputs.keys()):
            i = _WorkflowTokenAttribute()
            i._name = k
            wrap = ITypedValue(inputs[k])
            i._type = wrap.type()
            i._value = wrap.value()
            real_inputs.append(i)
        return real_inputs

    def executeWorkflow(self, wf, inputs={}):
        """Run a workflow with specified set of inputs.

        :param wf: workflow to run
        :type wf: vmw.vco.client.Workflow
        :param inputs: inputs to run with
        :type inputs: dict
        """
        return self._executeWorkflow(workflowId=wf.id,
                                     workflowInputs=self.__readInputs(inputs))

    def simpleExecuteWorkflow(self, wf, encoded_input):
        """**deprecated**

        Alternate way of executing a workflow. This will encode inputs in an
        unsafe way, please don't use.

        :param wf: workflow to run
        :type wf: vmw.vco.client.Workflow
        :param inputs: inputs to run with
        :type inputs: dict
        """
        return self._simpleExecuteWorkflow(in0=wf.id, in3=encoded_input)

    def getWorkflowTokenForId(self, token_id):
        """Retrieve a workflow token from its id.

        :param token_id: token id
        :type token_id: string
        """
        return self._getWorkflowTokenForId(workflowTokenId=token_id)

    def getWorkflowTokenResult(self, token):
        """Get result for workflow token. Only applies when the workflow execution is completed.

        :param token: token to extract result from
        :type token: vmw.vco.client.WorkflowToken
        """
        return self._getWorkflowTokenResult(workflowTokenId=token.id)

    def getWorkflowTokenStatus(self, tokens):
        """Get status for specified list of workflow tokens. Returns a list of
        status in the same order.
        """
        return self._getWorkflowTokenStatus(workflowTokenIds=[t.id for t in tokens])

    def answerWorkflowInput(self, token, inputs={}):
        """Provide answer for the user interaction the token is waiting on.

        :param token: workflow token to answer to
        :type token: vmw.vco.client.WorkflowToken
        :param inputs: input parameters to provide as an answer
        :type inputs: dict
        """
        return self._answerWorkflowInput(workflowTokenId=token.id,
                                         answerInputs=self.__readInputs(inputs))

    def hasRights(self, task, right):
        """Check if current user has rights over the specified task."""
        return self._hasRights(taskId=task.id, right=right)

    def sendCustomEvent(self, event, props):
        """Send a custom event with specified properties.

        :param event: event to send
        :type event: string
        :param props: properties of the event
        :type props: dict
        """
        props = "\n".join(["%s=%s" % (str(key), str(val))
                           for (key, val) in list(props.items())])
        return self._sendCustomEvent(eventName=event, serializedProperties=props)

    def find(self, type, query=""):
        """Find objects of a given type, that match a plug-in dependant query."""
        return self._find(type=type, query=query)

    def findForId(self, type, id):
        """Find specific object, from it's type and unique id."""
        try:
            return self._findForId(type=type, id=id)
        except EvaluateException:
            return None

    def findRelation(self, type, id, relation):
        """Find children of specific object (defined by its type and unique
        id), according to specified relation."""
        try:
            return self._findRelation(parentType=type, parentId=id,
                                      relationName=relation)
        except EvaluateException:
            return []

    def hasChildrenInRelation(self, type, id, relation):
        """Check if specified object (defined by its type and unique id) has
        any children according to specified relation."""
        return self._hasChildrenInRelation(parentType=type, parentId=id,
                                           relationName=relation)

    def echo(self, msg):
        """Test method. Echo back provided message.

        :param msg: Message to echo.
        :type msg: string
        """
        return self._echo(message=msg)

    def echoWorkflow(self, wf):
        """Test method. Echo back provided workflow.

        :param wf: Workflow to echo.
        :type wf: vmw.vco.client.Workflow
        """
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
        return dict([(t._name, TypedValue(t._type, t._value)) for t in res])

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
        return [FinderResult(self, r) for r in res._elements._item]

    def _findForIdTrans(self, res):
        return FinderResult(self, res)

    def _findRelationTrans(self, res):
        return [FinderResult(self, r) for r in res]

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
            keys = list(keywords.keys())
            # build the request object with all specified components
            for kw in keys:
                setattr(req, "_" + kw, keywords[kw])

            # call the generated method, and get response
            resp = getattr(self.service, name)(req)

            def __extractRes(resp, name, trans):
                # extract relevant value from response object
                res = getattr(resp, "_" + name + "Return", None)
                # optionally transform result
                if trans:
                    return trans(res)
                else:
                    return res

            if TWISTED_PRESENT and isinstance(resp, Deferred):
                resp.addCallback(__extractRes, name, trans)
                return resp
            else:
                return __extractRes(resp, name, trans)

        # add the method to this object
        setattr(self, "_" + name, _func)

class TypedValue(object):
    implements(ITypedValue)

    def __init__(self, type, value):
        """Build a typed value

        :param type: type of the value
        :param value: string representation of the value
        """
        self._type = type
        self._value = value

    def type(self):
        return self._type

    def value(self):
        return self._value

class Plugin(object):
    def __init__(self, server, holder):
        self._server = server
        self._holder = holder

        #: Plugin name
        self.name = holder._moduleName
        #: Plugin description
        self.description = holder._moduleDescription
        self._repr = holder._moduleDisplayName
        #: Plugin version
        self.version = holder._moduleVersion

    def __repr__(self):
        return self._repr

class WorkflowAttribute(object):
    def __init__(self, server, holder):
        self._server = server
        self._holder = holder

        #: Attribute name
        self.name = holder._name
        #: Attribute type
        self.type = holder._type

class Workflow(object):
    def __init__(self, server, holder):
        self._server = server
        self._holder = holder

        #: Workflow id
        self.id = holder._id
        #: Workflow name
        self.name = holder._name
        #: Workflow description
        self.description = holder._description
        #: Workflow input parameters. list
        #: of :class:`vmw.vco.client.WorkflowAttribute`
        self.inParameters = self.__convertAttributes(holder._inParameters)
        #: Workflow output parameters. list
        #: of :class:`vmw.vco.client.WorkflowAttribute`
        self.outParameters = self.__convertAttributes(holder._outParameters)
        #: Workflow attributes. list
        #: of :class:`vmw.vco.client.WorkflowAttribute`
        self.attributes = self.__convertAttributes(holder._attributes)

    def __convertAttributes(self, attrs):
        return [WorkflowAttribute(self._server, it) for it in attrs._item]

    def execute(self, inputs={}):
        """Execute this workflow with provided input parameters.

        :param inputs: input parameters
        :type inputs: dict
        """
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
        self._server = server
        self._holder = holder

        #: WorkflowToken id
        self.id = holder._id
        #: WorkflowToken title
        self.title = holder._title
        #: Related Workflow id
        self.workflowId = holder._workflowId
        self.currentItemName = holder._currentItemName
        self.currentItemState = holder._currentItemState
        #: WorkflowToken state
        self.globalState = holder._globalState
        self.startDate = holder._startDate
        self.endDate = holder._endDate
        self.xmlContent = holder._xmlContent

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
            self.__wait(self.isWaiting, poll, d)
            return d.addCallback(lambda _: self)
        else:
            self.__wait(self.isWaiting, poll)
            return self

    def answer(self, inputs):
        return self._server.answerWorkflowInput(self, inputs)

class Rights(object):
    READ = ord('r')
    WRITE = ord('c')
    EXECUTE = ord('x')

class FinderResult(object):

    implements(ITypedValue)

    def __init__(self, server, holder):
        self._server = server
        self._holder = holder

        #: FinderResult id
        self.id = holder._id
        #: FinderResult uri
        self.uri = holder._dunesUri
        #: FinderResult properties (dict)
        self.properties = self.__readProperties(holder._properties)

    def __readProperties(self, props):
        res = {}
        for i in props._item:
            res[i._name] = i._value
        return res

    def type(self):
        return self._holder._type

    def value(self):
        return self.uri
