'''
一个node等价于一个service, node针对每个频道管理一个service organizer
脚本本身不考虑性能, 所以这里每个服务都存一份service info对象暂时认为是无所谓的
'''
from forward.edge_service import EdgeServiceInfo, EdgeServiceRole
from forward.service_organizer import Organizer

class Node:
    def __init__(self, edge: EdgeServiceInfo):
        self.channel_2_organizer = {}  # channel_id -> ServiceOrganizer
        self.services = {} # 当新的频道出现时, 使用这里的信息初始化一个organizer
        self._self_info = edge

    def InitWithEdgeList(self, edge_info_dict):
        self.services.clear()
        self.services.update(edge_info_dict)

    def AddService(self, service_info: EdgeServiceInfo):
        if self._self_info == service_info:
            return
        self.services[service_info.service_id] = service_info
        for organizer in self.channel_2_organizer.values():
            organizer.AddService(service_info)

    def AddChannel(self, cid: int, channel_name: str):
        self.channel_2_organizer[cid] = Organizer(self._self_info, cid)
        self.channel_2_organizer[cid].InitEdges(self.services)
    
    def GetDownsideStreamNodes(self, cid: int, uid: int, role: EdgeServiceRole):
        # cid级别分树
        if cid not in self.channel_2_organizer:
            return []
        return self.channel_2_organizer[cid].GetDownsideStreamNodes(uid, role)