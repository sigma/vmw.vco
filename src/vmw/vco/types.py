from generated.VSOWebControlService_types import ns0
from vmw.ZSI.schema import GTD

__schema = ns0.targetNamespace

def __getClass(name):
    return GTD(__schema, name)(name).pyclass

Workflow = __getClass("Workflow")
WorkflowToken = __getClass("WorkflowToken")
WorkflowTokenAttribute = __getClass("WorkflowTokenAttribute")
WorkflowParameter = __getClass("WorkflowParameter")
ArrayOfWorkflowParameter = __getClass("ArrayOfWorkflowParameter")
ModuleInfo = __getClass("ModuleInfo")
FinderResult = __getClass("FinderResult")
ArrayOfFinderResult = __getClass("ArrayOfFinderResult")
Property = __getClass("Property")
ArrayOfProperty = __getClass("ArrayOfProperty")
QueryResult = __getClass("QueryResult")
