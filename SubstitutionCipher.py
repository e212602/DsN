#!/usr/bin/python3
import threading
import sys
import os
import signal
from datetime import datetime
import argparse
from enum import Enum
import time
import random


def generate_key():
    letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" 
    key = {}
    for c in letters:
        r = random.randint(0,len(letters)-1)
        key[c] = letters[r]
        letters = letters.replace(letters[r],'')
    return key
    
    
class SubstitutionCipher:
    def __init__(self):
        pass
    
    def encrypt(self,msg,key:dict):
        cipher = ""
        for c in msg.upper():
            if c in key.keys():
                cipher = cipher + key[c]
            else:
                cipher += c
                
        return cipher
    
    def decrypt(self,cipher:None,key:dict):
        msg = ""
        for c in cipher:
            if c in key.values():
                for k,i in key.items():
                    if i == c:
                        msg = msg + k
                        break
            else:
                msg = msg + c
        return msg
    
if __name__ == "__main__":
    try:
        k = generate_key()
        sc = SubstitutionCipher()
        cipher = sc.encrypt("hello world", k)
        print(cipher)
        msg = sc.decrypt(cipher, k)
        print(msg)
        
    except Exception as e:
        print(e)