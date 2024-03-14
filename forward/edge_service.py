from utils.type_check import CheckValueTypeWithList
from enum import Enum

class EdgeServiceRole(Enum):
    kNormal = 0
    kBroadcastInMachine = 1
    kBroadcastInIdc = 2
    kBroadcastInContinent = 3
    kBroadcastInWorld = 4
    kRoleMax = 5

class EdgeServiceInfo:
    def __init__(self, continent:str, idc:str, machine_id:int, service_id:int) -> None:
        CheckValueTypeWithList([
            [continent, str],
            [idc, str],
            [machine_id, int],
            [service_id, int]
        ])
        self.continent = continent
        self.idc = idc
        self.machine_id = machine_id
        self.service_id = service_id

    def GetZoneKeyWithLevel(self, level: int):
        if level == 1:
            return self.continent
        elif level == 2:
            return self.idc
        elif level == 3:
            return self.machine_id
        elif level == 4:
            return self.service_id

class EdgeServiceWithRole:
    def __init__(self, edge_service_info: EdgeServiceInfo, role: EdgeServiceRole) -> None:
        self.edge_service_info: EdgeServiceInfo = edge_service_info
        self.role = role

