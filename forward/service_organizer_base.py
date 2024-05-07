import abc
from forward.edge_service import *
from forward.zone import *

class OrganizerInterface(metaclass=abc.ABCMeta):
    @abc.abstractmethod
    def AddService(self, edge_info: EdgeServiceInfo):
        pass
    
    @abc.abstractmethod
    def RemoveService(self, edge_info: EdgeServiceInfo):
        pass

    @abc.abstractmethod
    def GetDownsideStreamNodes(self, uid: int, role: EdgeServiceRole):
        pass