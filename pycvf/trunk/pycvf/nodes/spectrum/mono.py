# -*- coding: utf-8 -*-
###
### We assume that we have a sequence of spectro
### we do temporal blocks of spectros
### these temporal block may later be converted into image
### 

import numpy,sys,itertools
from pycvf.core import genericmodel
from pycvf.datatypes import basics
from pycvf.datatypes import audio
from pycvf.datatypes import histogram

class Model(genericmodel.Model):
        def input_datatype(self,x):
            #assert(isinstance(x,image.Datatype)), (str(type(x)) , "is not an image")
            #return .Datatype
            return x
        def output_datatype(self,x):
            #return basics.
            return x
        def init_model(self,blocksize=600,*args, **kwargs):
              self.processing=[ ('spectromono' , {'spectromono':lambda rdr:itertools.imap(lambda pkt:numpy.exp(((numpy.abs(pkt[:,0])+numpy.abs(pkt[:,0]))/2)*((numpy.angle(pkt[:,0])+numpy.angle(pkt[:,0])/)2)*1J),rdr)  })]

__call__=Model
