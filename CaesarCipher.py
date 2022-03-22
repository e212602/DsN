#!/usr/bin/python3
import threading
import sys
import os
import signal
from datetime import datetime
import argparse
from enum import Enum
import time



__Discription__ = "Ceasar Cipher"
__verions__ = "1.0"

def generate_key(n):
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    key = {}
    cnt = 0
    for c in letters:
        key[c] = letters[(cnt+n)%len(letters)]
        cnt += 1
    return key

class CaesarCipher:
    def __init__(self):
        pass
        
    def encrypt(self,msg:None,key:dict):
        cipher = ""
        for c in msg.upper():
            cipher = cipher + key[c]
        return cipher
    
    def decrypt(self,cipher:None,key:dict):
        msg = ""
        for c in cipher:
            for k,i in key.items():
                if i == c:
                    msg = msg + k
        return msg
        
        
class AntiCaesarCipher:
    def __init__(self):
        pass
    def Attack(self,cipher):
        cs = CaesarCipher()
        for i in range(26):
            k = generate_key(i)
            msg = cs.encrypt(cipher, k)
            print(msg)
            
              
        
if __name__ == "__main__":
    try:
        k = generate_key(1)
        cc = CaesarCipher()
        cipher = cc.encrypt("helloworld", k)
        print(cipher)
        # msg = cc.decrypt(cipher, k)
        # print(msg)
        
        # Attack
        eve = AntiCaesarCipher()
        eve.Attack(cipher)
    except Exception as e:
        print(e)
