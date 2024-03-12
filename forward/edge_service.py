from ..utils.type_check import CheckValueTypeWithList

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


    