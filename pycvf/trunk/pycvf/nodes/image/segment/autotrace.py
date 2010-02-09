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
from pycvf.datatypes import image
from pycvf.lib.graphics.autotrace import AutoTrace
from pycvf.structures.list import PointListStructure

import numpy
def normalz(img):
  return (((img-img.min())*255.)/img.ptp()).astype(numpy.uint8)


class Model(genericmodel.Model):
        def input_datatype(self,x):
            assert(isinstance(x,image.Datatype) or issubclass(x,image.Datatype))
            return image.Datatype
        def output_datatype(self,x):
            return list.Datatype(basics.UnhandledDatatype)
        def init_model(self,id="",normalize=True,*args,**kwargs):
                 self.processline='src|autotrace'+id
                 at=AutoTrace()
                 for k in self.kwargs.items():
                    exec "at.opts.contents.%s=v"%(k[0]) in {'at':at, 'v':k[1]}
                 def process(i):
                    r=at.trace(normalz(i))
                    return r.__dict__()['splines']
                 self.context['autotrace'+id]=process

__call__=Model