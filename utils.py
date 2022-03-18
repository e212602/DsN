import networkx as nx
from Node import Node

def dfs(G:nx,node:Node,vs=[]):
    if node == None:
        return

    vs.append(node)
    
    G.add_node(node.id)

    for n in node.GetNeighbours():
        if n in vs:
            continue
        G.add_edge(node.id,n.id)
        dfs(G,n,vs)

    return
