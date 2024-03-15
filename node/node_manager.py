'''
node manager是node的管理者, 在service中是没有的
'''
from forward.edge_service import EdgeServiceInfo, EdgeServiceRole
from utils.log import logger
from node.node import Node
from queue import Queue
from draw.painter import Painter

class NodeManager:
    def __init__(self):
        self.nodes = {}  # node_id -> Node 非异或node id
        self.services = {}  # edge_service_id -> EdgeServiceInfo 新加入的node需要这个信息去初始化

    def AddService(self, edge: EdgeServiceInfo):
        # 已有节点新增edge信息
        for node in self.nodes.values():
            node.AddService(edge)
        # 创建edge并初始化
        self.nodes[edge.service_id] = Node(edge)
        self.nodes[edge.service_id].InitWithEdgeList(self.services)
        # edge信息加入到services内
        self.services[edge.service_id] = edge

    def AddChannel(self, cid: int, channel_name: str):
        for node in self.nodes.values():
            node.AddChannel(cid, channel_name)

    def HashNodeWithRole(self, node_info):
        return "{}_{}".format(node_info[0], node_info[1])

    def CreateSpeaker(self, sid: int, cid: int, speaker_uid: int):
        # 画图
        pt = Painter()
        vis = {}  # node_id + role -> bool
        vis_sid = {}  # sid -> bool
        queue = Queue()
        init_nodes = self.nodes[sid].GetDownsideStreamNodes(cid, speaker_uid, EdgeServiceRole.kBroadcastInWorld)
        logger.debug(len(init_nodes))
        pt.AddNode(str(sid), 0)
        for node in init_nodes:  # node format: [sid, role]
            queue.put(node)
            logger.debug("find edge from:{}, to:{}, level:{}".format(sid, node[0], node[1]))
            vis[self.HashNodeWithRole(node)] = True
            if node[0] not in vis_sid.keys():
                vis_sid[node[0]] = True
                logger.debug("add node:{}, subset:{}".format(node[0], 4 - node[1].value))
                pt.AddNode(str(node[0]), 4 - node[1].value)
            pt.AddEdge(str(sid), str(node[0]))

        while not queue.empty():
            now_node, now_role = queue.get()  # sid , role
            next_node_list = self.nodes[now_node].GetDownsideStreamNodes(cid, speaker_uid, now_role)
            # logger.debug("now:{}_{} next:{}".format(
            #     now_node, now_role, next_node_list
            # ))
            for node in next_node_list:
                if not self.HashNodeWithRole(node) in vis.keys():
                    queue.put(node)
                    vis[self.HashNodeWithRole(node)] = True
                # 当一个node出现过时, 不代表别人不能连向它, 相反冗余发送本来就应该有点连向它
                logger.debug("find edge from:{}, to:{}, level:{}".format(now_node, node[0], node[1]))
                if node[0] not in vis_sid.keys():
                    vis_sid[node[0]] = True
                    logger.debug("add node:{}, subset:{}".format(node[0], 4 - node[1].value))
                    pt.AddNode(str(node[0]), 4 - node[1].value)
                pt.AddEdge(str(now_node), str(node[0]))

        pt.WriteDot()
        

    