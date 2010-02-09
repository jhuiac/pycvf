# -*- coding: utf-8 -*-
###
### We assume that we have a sequence of spectro
### we do temporal blocks of spectros
### these temporal block may later be converted into image
### 

import sys, itertools
from pycvf.core.genericmodel import pycvf_model_class
#from pycvf.datatypes import list as ldt
from pycvf.datatypes import generated

class Ngrams:
    def __init__(self,size=2):
        self.size=size
        self.lst=[]
    def process(self,origiter):
        class XIter:
            def __init__(silf):
                pass
            def __iter__(silf):
                if (not hasattr(origiter,"next")) and  (hasattr(origiter,"__iter__")):
                    it=iter(origiter)
                else:
                    it=origiter
                cont=True
                try:
                    r=[]
                    for x in range(self.size) :
                        r.append( it.next())                        
                    yield r
                    while True:
                        r.pop(0)
                        r.append( it.next())
                        yield r
                except StopIteration:
                   pass
        return iter(XIter())

Model=pycvf_model_class(None,lambda x:generated.Datatype(x) )(Ngrams)
__call__=Model
