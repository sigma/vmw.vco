##################################################
# file: VSOWebControlService_server.py
#
# skeleton generated by "vmw.ZSI.generate.wsdl2dispatch.ServiceModuleWriter"
#      /home/yann/.virtualenvs/test/bin/wsdl2py -o vmw/vco/generated/ -w resources/wsdl/vco.wsdl.tpl
#
##################################################

from vmw.ZSI.schema import GED, GTD
from vmw.ZSI.TCcompound import ComplexType, Struct
from VSOWebControlService_types import *
from vmw.ZSI.twisted.WSresource import WSResource

# Messages  
findRequest = GED("http://webservice.vso.dunes.ch", "find").pyclass

findResponse = GED("http://webservice.vso.dunes.ch", "findResponse").pyclass

echoRequest = GED("http://webservice.vso.dunes.ch", "echo").pyclass

echoResponse = GED("http://webservice.vso.dunes.ch", "echoResponse").pyclass

echoWorkflowRequest = GED("http://webservice.vso.dunes.ch", "echoWorkflow").pyclass

echoWorkflowResponse = GED("http://webservice.vso.dunes.ch", "echoWorkflowResponse").pyclass

sendCustomEventRequest = GED("http://webservice.vso.dunes.ch", "sendCustomEvent").pyclass

sendCustomEventResponse = GED("http://webservice.vso.dunes.ch", "sendCustomEventResponse").pyclass

getWorkflowForIdRequest = GED("http://webservice.vso.dunes.ch", "getWorkflowForId").pyclass

getWorkflowForIdResponse = GED("http://webservice.vso.dunes.ch", "getWorkflowForIdResponse").pyclass

getAllWorkflowsRequest = GED("http://webservice.vso.dunes.ch", "getAllWorkflows").pyclass

getAllWorkflowsResponse = GED("http://webservice.vso.dunes.ch", "getAllWorkflowsResponse").pyclass

getWorkflowsWithNameRequest = GED("http://webservice.vso.dunes.ch", "getWorkflowsWithName").pyclass

getWorkflowsWithNameResponse = GED("http://webservice.vso.dunes.ch", "getWorkflowsWithNameResponse").pyclass

executeWorkflowRequest = GED("http://webservice.vso.dunes.ch", "executeWorkflow").pyclass

executeWorkflowResponse = GED("http://webservice.vso.dunes.ch", "executeWorkflowResponse").pyclass

simpleExecuteWorkflowRequest = GED("http://webservice.vso.dunes.ch", "simpleExecuteWorkflow").pyclass

simpleExecuteWorkflowResponse = GED("http://webservice.vso.dunes.ch", "simpleExecuteWorkflowResponse").pyclass

cancelWorkflowRequest = GED("http://webservice.vso.dunes.ch", "cancelWorkflow").pyclass

cancelWorkflowResponse = GED("http://webservice.vso.dunes.ch", "cancelWorkflowResponse").pyclass

getWorkflowTokenResultRequest = GED("http://webservice.vso.dunes.ch", "getWorkflowTokenResult").pyclass

getWorkflowTokenResultResponse = GED("http://webservice.vso.dunes.ch", "getWorkflowTokenResultResponse").pyclass

getWorkflowTokenForIdRequest = GED("http://webservice.vso.dunes.ch", "getWorkflowTokenForId").pyclass

getWorkflowTokenForIdResponse = GED("http://webservice.vso.dunes.ch", "getWorkflowTokenForIdResponse").pyclass

getWorkflowTokenStatusRequest = GED("http://webservice.vso.dunes.ch", "getWorkflowTokenStatus").pyclass

getWorkflowTokenStatusResponse = GED("http://webservice.vso.dunes.ch", "getWorkflowTokenStatusResponse").pyclass

answerWorkflowInputRequest = GED("http://webservice.vso.dunes.ch", "answerWorkflowInput").pyclass

answerWorkflowInputResponse = GED("http://webservice.vso.dunes.ch", "answerWorkflowInputResponse").pyclass

hasRightsRequest = GED("http://webservice.vso.dunes.ch", "hasRights").pyclass

hasRightsResponse = GED("http://webservice.vso.dunes.ch", "hasRightsResponse").pyclass

getAllPluginRequest = GED("http://webservice.vso.dunes.ch", "getAllPlugin").pyclass

getAllPluginResponse = GED("http://webservice.vso.dunes.ch", "getAllPluginResponse").pyclass

getAllPluginsRequest = GED("http://webservice.vso.dunes.ch", "getAllPlugins").pyclass

getAllPluginsResponse = GED("http://webservice.vso.dunes.ch", "getAllPluginsResponse").pyclass

findForIdRequest = GED("http://webservice.vso.dunes.ch", "findForId").pyclass

findForIdResponse = GED("http://webservice.vso.dunes.ch", "findForIdResponse").pyclass

findRelationRequest = GED("http://webservice.vso.dunes.ch", "findRelation").pyclass

findRelationResponse = GED("http://webservice.vso.dunes.ch", "findRelationResponse").pyclass

hasChildrenInRelationRequest = GED("http://webservice.vso.dunes.ch", "hasChildrenInRelation").pyclass

hasChildrenInRelationResponse = GED("http://webservice.vso.dunes.ch", "hasChildrenInRelationResponse").pyclass


# Service Skeletons
class VSOWebControlService(WSResource):
    soapAction = {}
    root = {}

    def __init__(self, post='/vmware-vmo-webcontrol/webservice', **kw):
        WSResource.__init__(self)

    def soap_find(self, ps, **kw):
        request = ps.Parse(findRequest.typecode)
        return request,findResponse()

    soapAction[''] = 'soap_find'
    root[(findRequest.typecode.nspname,findRequest.typecode.pname)] = 'soap_find'

    def soap_echo(self, ps, **kw):
        request = ps.Parse(echoRequest.typecode)
        return request,echoResponse()

    soapAction[''] = 'soap_echo'
    root[(echoRequest.typecode.nspname,echoRequest.typecode.pname)] = 'soap_echo'

    def soap_echoWorkflow(self, ps, **kw):
        request = ps.Parse(echoWorkflowRequest.typecode)
        return request,echoWorkflowResponse()

    soapAction[''] = 'soap_echoWorkflow'
    root[(echoWorkflowRequest.typecode.nspname,echoWorkflowRequest.typecode.pname)] = 'soap_echoWorkflow'

    def soap_sendCustomEvent(self, ps, **kw):
        request = ps.Parse(sendCustomEventRequest.typecode)
        return request,sendCustomEventResponse()

    soapAction[''] = 'soap_sendCustomEvent'
    root[(sendCustomEventRequest.typecode.nspname,sendCustomEventRequest.typecode.pname)] = 'soap_sendCustomEvent'

    def soap_getWorkflowForId(self, ps, **kw):
        request = ps.Parse(getWorkflowForIdRequest.typecode)
        return request,getWorkflowForIdResponse()

    soapAction[''] = 'soap_getWorkflowForId'
    root[(getWorkflowForIdRequest.typecode.nspname,getWorkflowForIdRequest.typecode.pname)] = 'soap_getWorkflowForId'

    def soap_getAllWorkflows(self, ps, **kw):
        request = ps.Parse(getAllWorkflowsRequest.typecode)
        return request,getAllWorkflowsResponse()

    soapAction[''] = 'soap_getAllWorkflows'
    root[(getAllWorkflowsRequest.typecode.nspname,getAllWorkflowsRequest.typecode.pname)] = 'soap_getAllWorkflows'

    def soap_getWorkflowsWithName(self, ps, **kw):
        request = ps.Parse(getWorkflowsWithNameRequest.typecode)
        return request,getWorkflowsWithNameResponse()

    soapAction[''] = 'soap_getWorkflowsWithName'
    root[(getWorkflowsWithNameRequest.typecode.nspname,getWorkflowsWithNameRequest.typecode.pname)] = 'soap_getWorkflowsWithName'

    def soap_executeWorkflow(self, ps, **kw):
        request = ps.Parse(executeWorkflowRequest.typecode)
        return request,executeWorkflowResponse()

    soapAction[''] = 'soap_executeWorkflow'
    root[(executeWorkflowRequest.typecode.nspname,executeWorkflowRequest.typecode.pname)] = 'soap_executeWorkflow'

    def soap_simpleExecuteWorkflow(self, ps, **kw):
        request = ps.Parse(simpleExecuteWorkflowRequest.typecode)
        return request,simpleExecuteWorkflowResponse()

    soapAction[''] = 'soap_simpleExecuteWorkflow'
    root[(simpleExecuteWorkflowRequest.typecode.nspname,simpleExecuteWorkflowRequest.typecode.pname)] = 'soap_simpleExecuteWorkflow'

    def soap_cancelWorkflow(self, ps, **kw):
        request = ps.Parse(cancelWorkflowRequest.typecode)
        return request,cancelWorkflowResponse()

    soapAction[''] = 'soap_cancelWorkflow'
    root[(cancelWorkflowRequest.typecode.nspname,cancelWorkflowRequest.typecode.pname)] = 'soap_cancelWorkflow'

    def soap_getWorkflowTokenResult(self, ps, **kw):
        request = ps.Parse(getWorkflowTokenResultRequest.typecode)
        return request,getWorkflowTokenResultResponse()

    soapAction[''] = 'soap_getWorkflowTokenResult'
    root[(getWorkflowTokenResultRequest.typecode.nspname,getWorkflowTokenResultRequest.typecode.pname)] = 'soap_getWorkflowTokenResult'

    def soap_getWorkflowTokenForId(self, ps, **kw):
        request = ps.Parse(getWorkflowTokenForIdRequest.typecode)
        return request,getWorkflowTokenForIdResponse()

    soapAction[''] = 'soap_getWorkflowTokenForId'
    root[(getWorkflowTokenForIdRequest.typecode.nspname,getWorkflowTokenForIdRequest.typecode.pname)] = 'soap_getWorkflowTokenForId'

    def soap_getWorkflowTokenStatus(self, ps, **kw):
        request = ps.Parse(getWorkflowTokenStatusRequest.typecode)
        return request,getWorkflowTokenStatusResponse()

    soapAction[''] = 'soap_getWorkflowTokenStatus'
    root[(getWorkflowTokenStatusRequest.typecode.nspname,getWorkflowTokenStatusRequest.typecode.pname)] = 'soap_getWorkflowTokenStatus'

    def soap_answerWorkflowInput(self, ps, **kw):
        request = ps.Parse(answerWorkflowInputRequest.typecode)
        return request,answerWorkflowInputResponse()

    soapAction[''] = 'soap_answerWorkflowInput'
    root[(answerWorkflowInputRequest.typecode.nspname,answerWorkflowInputRequest.typecode.pname)] = 'soap_answerWorkflowInput'

    def soap_hasRights(self, ps, **kw):
        request = ps.Parse(hasRightsRequest.typecode)
        return request,hasRightsResponse()

    soapAction[''] = 'soap_hasRights'
    root[(hasRightsRequest.typecode.nspname,hasRightsRequest.typecode.pname)] = 'soap_hasRights'

    def soap_getAllPlugin(self, ps, **kw):
        request = ps.Parse(getAllPluginRequest.typecode)
        return request,getAllPluginResponse()

    soapAction[''] = 'soap_getAllPlugin'
    root[(getAllPluginRequest.typecode.nspname,getAllPluginRequest.typecode.pname)] = 'soap_getAllPlugin'

    def soap_getAllPlugins(self, ps, **kw):
        request = ps.Parse(getAllPluginsRequest.typecode)
        return request,getAllPluginsResponse()

    soapAction[''] = 'soap_getAllPlugins'
    root[(getAllPluginsRequest.typecode.nspname,getAllPluginsRequest.typecode.pname)] = 'soap_getAllPlugins'

    def soap_findForId(self, ps, **kw):
        request = ps.Parse(findForIdRequest.typecode)
        return request,findForIdResponse()

    soapAction[''] = 'soap_findForId'
    root[(findForIdRequest.typecode.nspname,findForIdRequest.typecode.pname)] = 'soap_findForId'

    def soap_findRelation(self, ps, **kw):
        request = ps.Parse(findRelationRequest.typecode)
        return request,findRelationResponse()

    soapAction[''] = 'soap_findRelation'
    root[(findRelationRequest.typecode.nspname,findRelationRequest.typecode.pname)] = 'soap_findRelation'

    def soap_hasChildrenInRelation(self, ps, **kw):
        request = ps.Parse(hasChildrenInRelationRequest.typecode)
        return request,hasChildrenInRelationResponse()

    soapAction[''] = 'soap_hasChildrenInRelation'
    root[(hasChildrenInRelationRequest.typecode.nspname,hasChildrenInRelationRequest.typecode.pname)] = 'soap_hasChildrenInRelation'

