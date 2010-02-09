# -*- coding: utf-8 -*-
#########################################################################################################################################
#
# MyModel By Bertrand NOUVEL
# 2009 CNRS Postdoctorate JFLI
#
# (c) All rights reserved
# ###############################################
#
################################################################################################################################################################################
# Includes
################################################################################################################################################################################


###
###

from pycvf.core.errors import *
from pycvf.core import genericmodel
from pycvf.datatypes import basics
from pycvf.datatypes import list as ldt
from pycvf.datatypes import image
from pycvf.lib.graphics.autotrace import AutoTrace
from pycvf.structures.list import PointListStructure

import numpy
def normalz(img):
  return (((img-img.min())*255.)/img.ptp()).astype(numpy.uint8)

class AutoTracer:
    def __init__(self,**kwargs):
        self.at=AutoTrace()
        for k in kwargs.items():
                    exec "at.opts.contents.%s=v"%(k[0]) in {'at':self.at, 'v':k[1]}        
    def process(self,i):
        r=self.at.trace(normalz(i))
        #return r.__dict__()['splines']
        return r

@genericmodel.pycvf_model_function(basics.Label.Datatype,basics.Label.Datatype)    
def background_color(r):
    return r.get_object().get_background_color()

@genericmodel.pycvf_model_function(basics.Label.Datatype,basics.Label.Datatype)    
def splines(r):
    return r.get_object().get_splines()

Model=genericmodel.pycvf_model_class(image.Datatype,basics.Label.Datatype)(AutoTracer)
__call__=Model
