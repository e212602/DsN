#!/usr/bin/python3
import threading
import sys
import os
import signal
from datetime import datetime
import argparse
from enum import Enum
import time
from itertools import permutations 



__Discription__ = "Crypto Math Utils Demo"
__verions__ = "1.0"



                    
if __name__ == "__main__":
    try:
        my_list = ["hello","world","it's", "me"]
        list_of_permutations = permutations(my_list)
        for i in list_of_permutations:
            print(i)
    except Exception as e:
        print(e)
