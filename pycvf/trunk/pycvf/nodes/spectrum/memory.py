# -*- coding: utf-8 -*-
###
### We assume that we have a sequence of spectro
### we do temporal blocks of spectros
### these temporal block may later be converted into image
### 

import numpy, scipy,sys
from pycvf.core.genericmodel import pycvf_model_class
from pycvf.datatypes import basics
from pycvf.datatypes import audio
from pycvf.datatypes import histogram


class Spectromemory():
    def __init__(self,blocksize=60):
        self.blocksize=blocksize
        self.packetlist=[]
    def process(self,origiter):
        class XIter:
            def __init__(silf):
                pass
            def __iter__(silf):
                cont=True
                blk=0
                try:
                    r=[]
                    for x in range(self.blocksize) :
                        r.append( origiter.next())                        
                    yield r
                    while True:
                        r.pop(0)
                        r.append( origiter.next())
                        yield r
                except StopIteration:
                   pass
        return iter(XIter())

Model=pycvf_model_class(None,None)(Spectromemory)
__call__=Model
