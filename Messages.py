from enum import Enum
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

class Protocol(Enum):
  TEST = "Testmsg"
  ETST = "Encmsg"
  CLNG = "Challenge"
  RESP = "Response"
  AUTH = "AuthenticationRequest"



class Hash(Enum):
    RSA = 0
    AES = 1


@dataclass
class Header:
    Src : int
    Dist : int
    Pro : Protocol
    hash : Optional[Hash] = None
    Length : Optional[int] = None
    rndkey : Optional[int] = None

@dataclass
class Message:
    Hdr : Header
    payload : str
