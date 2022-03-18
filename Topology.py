import networkx as nx
import Node

class Topology:
    def __init__(self,G:nx.Graph):
        self._nodes = {}
        self._channels =  {}

        self.G = G
        nodes = list(G.nodes)
        channels = list(G.edges)
        for n in nodes:
            self._nodes[n] = Node.Node(n)

        for ch in channels:
            self._nodes[ch[0]].addNeighbour(self._nodes[ch[1]])
            self._nodes[ch[1]].addNeighbour(self._nodes[ch[0]])

    def GetRoot(self):
        return self._nodes[0]

    def GetNode(self,id):
        return self._nodes[id]

    def AddNode(self,n):
        self._nodes[n.id] = n