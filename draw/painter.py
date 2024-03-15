
import networkx as nx
import matplotlib.pyplot as plt
import os

class Painter:
    def __init__(self) -> None:
        # 使用无向图
        self.G = nx.DiGraph()
    
    def Clear(self):
        self.G.clear()
    
    def AddNode(self, name: str, level: int):
        self.G.add_node(name, subset=level)
    
    def AddEdge(self, from_s: str, to_s: str):
        self.G.add_edge(from_s, to_s)
    
    def Show(self):
        pos = nx.multipartite_layout(self.G)
        nx.draw_networkx(self.G, node_size = 1000, pos = pos, with_labels = True)
        plt.show()
    
    def WriteDot(self):
        real_path = os.path.dirname(os.path.realpath(__file__))
        nx.drawing.nx_pydot.write_dot(self.G, real_path + "/../dot/graph.dot")
