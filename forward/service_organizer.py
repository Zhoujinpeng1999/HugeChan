'''
后续若需对比不同算法, 这里可以用类似abc抽象接口
'''
from forward.edge_service import *
from forward.zone import *
from utils.random_hash import GenerateRandomKey
from utils.log import logger

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
        self.super_nodes: list[dict[int, EdgeServiceWithRole]] = [{},{},{},{},{}]
    
    def LOCAL_LOG_DEBUG(self,string: str):
        if self.self_edge.service_id == 100001:
            logger.debug("[Organizer: local_cid:{cid}, _rnd:{rnd}]:{mes}".format(
                cid=self.local_cid,
                rnd=self._rnd,
                mes=string
            ))
    def LOCAL_LOG_INFO(self,string: str):
        if self.self_edge.service_id == 100001:
            logger.info("[Organizer: local_cid:{cid}, _rnd:{rnd}]:{mes}".format(
                cid=self.local_cid,
                rnd=self._rnd,
                mes=string
            ))

    def AddService(self, now_edge: EdgeServiceInfo):
        # 先在services里新增
        xor_now_edge_sid = now_edge.service_id ^ self._rnd
        self.services[xor_now_edge_sid] = now_edge
        now_zone: Zone = self.root_zone
        for i in range(Level.kWorld.value, Level.kZoneMax.value-1):
            # 找到下一个Zone
            next_level = i+1
            next_zone_key = now_edge.GetZoneKeyWithLevel(next_level)
            if next_zone_key not in now_zone.children.keys():
                now_zone.children[next_zone_key] = Zone(next_level, now_zone, next_zone_key)
            now_zone = now_zone.children[next_zone_key]
            # 新增enable service
            now_zone.enabled_services[xor_now_edge_sid] = now_edge.service_id
            # 判断是否now_edge和self的分叉点
            if next_zone_key != self.self_edge.GetZoneKeyWithLevel(next_level):
                # 判断当前zone的super node是否不满
                self.LOCAL_LOG_DEBUG("next_zone: {}, level:{}".format(next_zone_key, next_level))
                if len(now_zone.super_nodes) < kLevelMaxSuperNode[next_level]:
                    now_zone.super_nodes[xor_now_edge_sid] = now_edge.machine_id
                    self.AddSuperNode(now_edge, next_level)
                else:
                    # 如果满了考虑取xor值最小的
                    now_keys = list(now_zone.super_nodes.keys())
                    self.LOCAL_LOG_DEBUG("keys:{}, sid:{}, xor_sid:{}".format(now_keys, now_edge.service_id, xor_now_edge_sid))
                    if xor_now_edge_sid < now_keys[0]:
                        self.RemoveSuperNode(self.services[now_keys[0]], next_level)
                        now_zone.super_nodes.pop(now_keys[0])
                        now_zone.super_nodes[xor_now_edge_sid] = now_edge.machine_id 
                        self.AddSuperNode(now_edge, next_level)
                break
        self.LOCAL_LOG_DEBUG("add service down")


    def AddSuperNode(self, edge_info: EdgeServiceInfo, level: int):
        reverse_idx = Level.kZoneMax.value - level  # 自己上一级在EdgeServiceRole中的位置
        self_role = reverse_idx - 1  # 计算自己在EdgeServiceRole中的位置
        temp_xor_service_id = edge_info.service_id ^ self._rnd
        # 检查当前service是否存在
        if not temp_xor_service_id in self.services.keys():
            self.LOCAL_LOG_INFO("service:{} not exist".format(
                edge_info.service_id
            ))
            return
        # 更新super node, 从它父亲级别开始, 因为它父亲级别下发的时候需要下发到他
        for i in range(reverse_idx, EdgeServiceRole.kRoleMax.value):
            temp_service_with_role = EdgeServiceWithRole(edge_info, EdgeServiceRole(self_role))
            self.super_nodes[i][temp_xor_service_id] = temp_service_with_role

    def RemoveSuperNode(self, edge_info: EdgeServiceInfo, level: int):
        reverse_idx = Level.kZoneMax.value - level  # 自己上一级在EdgeServiceRole中的位置
        temp_xor_service_id = edge_info.service_id ^ self._rnd
        # 在父以上super node中删除
        for i in range(reverse_idx, EdgeServiceRole.kRoleMax.value):
            self.super_nodes[i].pop(temp_xor_service_id)

    def RemoveService(self, edge_info: EdgeServiceInfo):
        pass

    def InitEdges(self, edge_info_dict: dict[int, EdgeServiceInfo]):
        for edge_info in edge_info_dict.values():
            self.AddService(edge_info)

    def GetDownsideStreamNodes(self, uid: int, role: EdgeServiceRole):
        ll = []
        for item in self.super_nodes[role.value].values():
            ll.append([item.edge_service_info.service_id, item.role, item.edge_service_info.GetZoneKeyWithLevel(4-item.role.value)])
        return ll
