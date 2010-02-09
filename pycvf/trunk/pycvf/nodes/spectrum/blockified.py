# -*- coding: utf-8 -*-
###
### We assume that we have a sequence of spectro
### we do temporal blocks of spectros
### these temporal block may later be converted into image
### 

import numpy, scipy,sys
from pycvf.core import genericmodel
from pycvf.datatypes import basics
from pycvf.datatypes import audio
from pycvf.datatypes import histogram


class Spectroblock():
    def __init__(self,blocksize):
        self.blocksize=blocksize
        self.packetlist=[]
    def push(self,origiter):
        class XIter:
            def __init__(silf):
                pass
            def __iter__(silf):
                cont=True
                blk=0
                while cont:
                   try:
                       r=[]
                       for x in range(self.blocksize) :
                           r.append( origiter.next())
                       blk+=1
                       #print "blk=",blk, len(r)
                       yield r
                   except StopIteration:
                       cont=False
                if (len(r)):
                    #print "blk=",blk ,len(r)                                       
                    yield r
                raise StopIteration                    
        return iter(XIter())



class Model(genericmodel.Model):
        def input_datatype(self,x):
            #assert(isinstance(x,image.Datatype)), (str(type(x)) , "is not an image")
            #return .Datatype
            return x
        def output_datatype(self,x):
            #return basics.
            return x
        def init_model(self,blocksize=600,*args, **kwargs):
              sb=Spectroblock(blocksize)
              self.processing=[ ('spectroblock' , {'spectroblock':sb.push })]

__call__=Model
