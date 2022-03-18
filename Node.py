from threading import Thread, Lock
import queue
import os
from enum import Enum
from Messages import *
import hashlib
from cryptography.hazmat.primitives.ciphers import (
    Cipher, algorithms, modes
)

class Node:
    def __init__(self,id):
        self.id = id
        self._neighbours = {}
        self.R = {}
        self.eventhandlers = {Protocol.TEST: self.TestHandler,
                              Protocol.ETST: self.EncTestMsgHandler,
                              Protocol.AUTH: self.Challenge, 
                              Protocol.CLNG: self.Response, 
                              Protocol.RESP: self.ResponseHandler}
        self.inputqueue = queue.Queue()
        th = Thread(target=self.queue_handler, args=[self.inputqueue])
        th.daemon = True
        th.start()
        

    def GetNeighbours(self):
        return self._neighbours.values()

    def addNeighbour(self,n):
        self._neighbours[n.id] = n

    def queue_handler(self, myqueue):
        while True:
          msg = myqueue.get()
          if msg.Hdr.Pro in self.eventhandlers:
            self.eventhandlers[msg.Hdr.Pro](msg=msg)  # call the handler
          else:
            print(f"Event Handler: {msg.Hdr.Protocol} is not implemented")
          myqueue.task_done()

    def TestHandler(self, msg: Message):
        print(f"{self.id} recieved a message from {msg.Hdr.Src}: {m}")
        pass

    def PutMsg(self,msg:Message):
        self.inputqueue.put_nowait(msg)

    def CreateMsg(self,Dist,Protocol,payload,hash):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.OFB(iv))
        encryptor = cipher.encryptor()
        ct = encryptor.update(bytes(payload,"utf-8")) + encryptor.finalize()

        msg = Message(
            Hdr = Header(Src = self.id,
                         Dist = Dist.id,
                         Pro = Protocol,
                         hash = hash,
                         rndkey = iv
                         ),
            payload = ct
        )

        return msg

    def Sendmsg(self,msg:Message):
        if msg.Hdr.Dist in self._neighbours.keys():
            self._neighbours[msg.Hdr.Dist].PutMsg(msg)
        else:
            print(f"No channel found with {msg.Hdr.Dist}")

    def EncTestMsgHandler(self, msg: Message):
        iv = msg.Hdr.rndkey
        cipher = Cipher(algorithms.AES(self.key), modes.OFB(iv))
        try:
            decryptor = cipher.decryptor()
            m = decryptor.update(msg.payload) + decryptor.finalize()
            m = m.decode("utf-8")
            print(f"{self.id} recieved a message from {msg.Hdr.Src}: {m}")
        except:
            print("Could not Decrypt")
            pass
    
    def run(self,test:Protocol):
        if test == Protocol.TEST:
            for i in self.GetNeighbours():
                msg = self.CreateMsg(i,Protocol.TEST,"This is a Test Message", Hash.AES)
                self.Sendmsg(msg)

        elif test == Protocol.ETST:
            for i in self.GetNeighbours():
                msg = self.CreateMsg(i,Protocol.ETST,"This is an Encryption Test", Hash.AES)
                self.Sendmsg(msg)
        elif test == Protocol.AUTH:
            for i in self.GetNeighbours():
                self.AuthRequest(i)

    def addKey(self,key):
        self.key = key

    def Challenge(self,msg: Message):
        self.R[msg.Hdr.Src] = os.urandom(16)
        msg = Message(
            Hdr = Header(Src = self.id,
                         Dist = msg.Hdr.Src,
                         Pro = Protocol.CLNG
                         ),
            payload = self.R[msg.Hdr.Src]
        )
        self.Sendmsg(msg)

    def Response(self,msg: Message):
        iv = os.urandom(16)
        cipher = Cipher(algorithms.AES(self.key), modes.OFB(iv))
        encryptor = cipher.encryptor()
        ct = encryptor.update(msg.payload) + encryptor.finalize()

        msg = Message(
            Hdr = Header(Src = self.id,
                         Dist = msg.Hdr.Src,
                         Pro = Protocol.RESP,
                         hash = Hash.AES,
                         rndkey = iv
                         ),
            payload = ct
        )
        self.Sendmsg(msg)

    def ResponseHandler(self,msg: Message):
        iv = msg.Hdr.rndkey
        cipher = Cipher(algorithms.AES(self.key), modes.OFB(iv))
        try:
            decryptor = cipher.decryptor()
            m = decryptor.update(msg.payload) + decryptor.finalize()
            if m == self.R[msg.Hdr.Src]:
                print(f"{msg.Hdr.Src} is authenticated")
            else:
                print(f"{msg.Hdr.Src} is NOT authenticated")
            self.R.pop(msg.Hdr.Src)

        except:
            self.R.pop(msg.Hdr.Src)
            print("Could not Decrypt")
            pass

    def AuthRequest(self,Dist):
        msg = Message(
            Hdr = Header(Src = self.id,
                         Dist = Dist.id,
                         Pro = Protocol.AUTH
                         ),
            payload = ""
        )
        self.Sendmsg(msg)
