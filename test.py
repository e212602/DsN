#!/usr/bin/python3
import threading
import sys
import os
import signal
from datetime import datetime
import argparse
from enum import Enum
import networkx as nx
import matplotlib.pyplot as plt
import time
from Topology import Topology
from  utils import *
from Messages import *
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)




__version__ = "Demo"



if __name__ == "__main__":
    try:
        #G = nx.random_geometric_graph(10,0.5)
        #nx.draw(G, with_labels=True, font_weight='bold')
        #plt.draw()
        #topo = Topology(G)
        
        #root = topo.GetRoot()
        #for i in topo.GetRoot().GetNeighbours():
        #    msg = root.CreateMsg(i,Protocol.TEST,"Hi")
        #    root.Sendmsg(msg)
            
        #plt.show()
        #key = os.urandom(32)
        #iv = os.urandom(16)
        #cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
        #encryptor = cipher.encryptor()
        #ct = encryptor.update(b"a secret message") + encryptor.finalize()
        #decryptor = cipher.decryptor()
        #m = decryptor.update(ct) + decryptor.finalize()
        #print(m.decode("utf-8"))

        G=nx.Graph()
        G.add_node(0)
        G.add_node(1)
        G.add_node(2)
        G.add_edge(0,1)
        G.add_edge(1,2)
        G.add_edge(0,2)
        nx.draw(G, with_labels=True, font_weight='bold')
        plt.draw()
        key = os.urandom(32)
        topo = Topology(G)
        #for i in topo.GetNodes():
            #i.addKey(key[i.id])
        topo.GetNode(0).addKey(key)
        topo.GetNode(1).addKey(key)
        
        #topo.GetRoot().run(Protocol.AUTH)
        plt.show()


    except Exception as e:
        print(e)
