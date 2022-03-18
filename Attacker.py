from threading import Thread, Lock
import queue
import os
from enum import Enum
from Messages import *
import hashlib
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)
from Node import Node


class Attacker(Node):
    def __init__(self,id):
        super().__init__(id)
        self.Dist = 0
    
    
    def Response(self,msg: Message):
        msg = Message(
            Hdr = Header(Src = self.id,
                         Dist = 1,
                         Pro = Protocol.CLNG
                         ),
            payload = msg.payload
        )
        self.Sendmsg(msg)
        

    def ResponseHandler(self,msg: Message):
        msg = Message(
            Hdr = Header(Src = self.id,
                         Dist = self.Dist.id,
                         Pro = msg.Hdr.Pro,
                         hash = msg.Hdr.hash,
                         rndkey = msg.Hdr.rndkey
                         ),
            payload = msg.payload
        )
        self.Sendmsg(msg)


    def RelayAttack(self,Dist):
        self.Dist = Dist
        self.AuthRequest(self.Dist)
        
