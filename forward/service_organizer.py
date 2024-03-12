from edge_service import EdgeServiceInfo
from zone import *
from ..utils.random_hash import GenerateRandomKey

class Organizer:
    def __init__(self, self_edge: EdgeServiceInfo, local_cid:int):
        CheckValueTypeWithList([
            [self_edge, EdgeServiceInfo],
            [local_cid, int]
        ])
        self.self_edge = self_edge
        self.local_cid = local_cid
        self._rnd = GenerateRandomKey(local_cid)
        self.services: dict[int, EdgeServiceInfo] = {}
        self.root_zone: Zone = Zone(0, None, "world")
        self.super_nodes: list[dict[int, EdgeServiceInfo]] = [{},{},{},{},{}]
    
    def AddService(self, now_edge: EdgeServiceInfo):
        # 先在services里新增
        xor_now_edge_sid = now_edge.service_id ^ self._rnd
        self.services[xor_now_edge_sid] = now_edge
        now_zone:Zone = self.root_zone
        for i in range(Level.kWorld, Level.kZoneMax-1):
            # 找到下一个Zone
            next_level = i+1
            next_zone_key = now_edge.GetZoneKeyWithLevel(next_level)
            if next_zone_key not in now_zone.children.keys():
                now_zone.children[next_zone_key] = Zone(next_level, now_zone, next_zone_key)
            now_zone = now_zone.children[next_zone_key]

            # 新增enable service
            now_zone.enabled_services[xor_now_edge_sid] = now_edge.service_id
            # 判断是否now_edge和self的分叉点
            if next_zone_key != self.self_edge.GetZoneKeyWithLevel[next_level]:
                # 判断当前zone的super node是否不满
                if len(now_zone.super_nodes) < kLevelMaxSuperNode[i]:
                    now_zone.super_nodes[xor_now_edge_sid] = now_edge.machine_id
                    self.AddSuperNode(now_edge, next_level)
                # 如果满了考虑取xor值最小的
                now_keys = now_zone.super_nodes.keys()
                if xor_now_edge_sid < now_keys[-1]:
                    self.RemoveSuperNode(self.services[now_keys[-1]], next_level)
                    now_zone.super_nodes.pop(now_keys[-1])
                    now_zone.super_nodes[xor_now_edge_sid] = now_edge.machine_id
                    self.AddSuperNode(now_edge, next_level)




    def AddSuperNode(self, edge_info: EdgeServiceInfo, level: int):
        pass

    def RemoveSuperNode(self, edge_info: EdgeServiceInfo, level: int):
        pass