
import networkx as nx
import matplotlib.pyplot as plt

class Painter:
    def __init__(self) -> None:
        # 使用无向图
        self.G = nx.DiGraph()
    
    def Clear(self):
        self.G.clear()
    
    def AddNode(self, name: str, level: int):
        self.G.add_node(name, subset=level)
    
    def Show(self):
        pos = nx.multipartite_layout(self.G)
        nx.draw_networkx(self.G, node_size = 1000, pos = pos, with_labels = True)
        plt.show()
